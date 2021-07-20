import os
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import Result
from qleader.fci.fci_H2 import get_fci, get_minimum_distance
from google.oauth2 import id_token
from google.auth.transport import requests

from qleader.initializers import create_result
import json


@api_view(["GET", "POST"])
def result_list(request):

    if request.method == "GET":
        return Response()
    elif request.method == "POST":
        data_dict = json.loads(request.data)
        try:
            result = create_result(data_dict)
            return Response(result.id, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def home(request):

    if request.method == "GET":
        runs = Result.objects.all().order_by("created")
        # Here we can filter the list before displaying
        return Response(
            {
                "runs": runs.values(),
                "path_prefix": request.headers.get("PathPrefix", ""),
            },
            template_name="home.html",
        )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def detail(request, result_id):

    if request.method == "GET":
        result = Result.objects.filter(id=result_id)[0]
        runs = result.get_runs()

        distances = [results.distance for results in runs]
        energies = [results.energy for results in runs]
        iteration_energies = [results.get_iteration_energies() for results in runs]

        fci_distances, fci_energies = zip(*get_fci("def2-QZVPPD"))

        name = " ".join([result.basis_set, result.transformation])

        return Response(
            {
                "result": result,
                "runs_all": runs,
                "name": name,
                "energies": energies,
                "distances": distances,
                "iterationEnergies": iteration_energies,
                "fci_distances": list(fci_distances),
                "fci_energies": list(fci_energies),
                "path_prefix": request.headers.get("PathPrefix", ""),
            },
            template_name="detail.html",
        )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def leaderboard(request, *args, **kwargs):
    result_list = kwargs.get("result_list", None)
    criterion = kwargs.get("criterion", None)
    if criterion == "closest_minimum":
        list_name = "Closest minimums to \"FCI def2_QZVPPD\" minimal energy bond distance "
    elif criterion == "smallest_variance":
        list_name = "Smallest variances from \"FCI def2_QZVPPD\""
    elif not criterion:
        return redirect("/")
    else:
        list_name = "Minimum energies"
    return Response(
        {
            "results": result_list,
            "list_name": list_name,
            "criterion": criterion,
            "path_prefix": request.headers.get("PathPrefix", ""),
        },
        template_name="leaderboard.html",
    )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def invoke_leaderboard(request, criterion):

    if criterion == "closest_minimum":
        result_list = list(Result.objects.all())
        true_bond_distance = get_minimum_distance("def2-QZVPPD")
        result_list.sort(key=lambda x: x.min_energy_distance-true_bond_distance)
    elif criterion == "smallest_variance":
        result_list = Result.objects.order_by("variance_from_fci")[:10]
    else:
        criterion = "min_energy"
        result_list = Result.objects.order_by("min_energy")[:10]

    return leaderboard(request._request, result_list=result_list, criterion=criterion)

@api_view(["GET", "POST"])
@renderer_classes([TemplateHTMLRenderer])
def login(request):

    if request.method == "POST":
        try:
            token = request.data["credential"]
            body_csrf_token = request.data["g_csrf_token"]
            cookie_csrf_token = request.COOKIES["g_csrf_token"]

            # Make sure csrf tokens match
            if not body_csrf_token:
                raise ValueError("No CSRF token in body")
            if not cookie_csrf_token:
                raise ValueError("No CSRF token in cookie")
            if body_csrf_token != cookie_csrf_token:
                raise ValueError("Failed to verify double submit cookie")

            # Make sure JWT is valid.
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.environ.get("GOOGLE_CLIENT_ID"))

            print(f'"Log in" success, email is {idinfo["email"]}')
            # Log in or create a user or whatever from here.
        except ValueError:
            # Invalid token
            pass

        return redirect("/")
    elif request.method == "GET":
        return Response(
        {
            "google_client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "path_prefix": request.headers.get("PathPrefix", ""),
        },
        template_name="login.html"
        )
    
