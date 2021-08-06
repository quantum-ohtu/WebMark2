from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from qleader.models import Result
import qleader.fci.fci_H2 as fci
import qleader.hf.hf_H2 as hf
import numpy as np


from qleader.initializers import create_result
import json


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def result_receiver(request):

    if request.method == "GET":
        return Response()
    elif request.method == "POST":
        data_dict = json.loads(request.data)
        user = request.user
        try:
            result = create_result(data_dict, user)
            return Response(result.id, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_result(request, result_id):
    result = Result.objects.get(id=result_id)

    if result.public is False and result.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    res = result.get_dump()
    return Response(json.dumps(res), status=status.HTTP_200_OK)


@api_view(["GET"])
def get_leaderboard_distances(request):
    if request.method == "GET":
        distances = [round(x, 2) for x in np.linspace(0.1, 2, 20)]
        return Response(distances)


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def home(request):

    if request.method == "GET":
        results = Result.objects.all().order_by("created")

        # make own_results
        if (request.user.id is not None):
            token = Token.objects.get(user=request.user)
            own_results = results.filter(user=Token.objects.get(key=str(token)).user)
        else:
            own_results = results.filter(user=None)

        # filter results to only include own results and public other results
        filtered_results = results.filter(public=True).union(own_results)

        return Response(
            {
                "results": filtered_results.values(
                    'id',
                    'basis_set',
                    'transformation',
                    'optimizer',
                    'created',
                    'user__username'
                ),
                "own_results": own_results.values(),
                "path_prefix": request.headers.get("SCRIPT_NAME", ""),
            },
            template_name="home.html",
        )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def detail(request, result_id):

    try:
        result = Result.objects.get(id=result_id)
    except Exception as error:
        return Response({"error": repr(error)}, status.HTTP_404_NOT_FOUND, template_name="detail.html")

    if not result.public and result.user != request.user:
        raise PermissionDenied

    if request.method == "GET":
        runs = result.get_runs()
        distances = [results.distance for results in runs]
        energies = [results.energy for results in runs]
        iteration_energies = [results.get_iteration_energies() for results in runs]
        fci_distances, fci_energies = zip(*fci.get_fci("def2-QZVPPD"))
        name = " ".join([result.basis_set, result.transformation])

        return Response(
            {
                "result": result,
                "runs": runs,
                "name": name,
                "energies": energies,
                "distances": distances,
                "iterationEnergies": iteration_energies,
                "fci_distances": list(fci_distances),
                "fci_energies": list(fci_energies),
                "path_prefix": request.headers.get("SCRIPT_NAME", ""),
            },
            template_name="detail.html",
        )


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def remove_result(request, result_id):

    try:
        result = Result.objects.get(id=result_id)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == "DELETE":
        if result.user == request.user:
            result.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def change_publicity(request, result_id):
    try:
        result = Result.objects.get(id=result_id)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == "POST":
        if result.user == request.user:
            result.public = request.data['boolean']
            result.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def compare_detail(request):
    result_ids = request.GET.getlist('id[]')
    results = Result.objects.filter(id__in=result_ids)
    run_list = [result.get_runs() for result in results]

    distances = [[results.distance for results in run] for run in run_list]
    energies = [[results.energy for results in run] for run in run_list]

    fci_distances, fci_energies = zip(*fci.get_fci("def2-QZVPPD"))

    names = ["_".join([result.basis_set, result.transformation, result.optimizer]) for result in results]
    ids = [result.id for result in results]

    # Only start gathering information for the error vs ciruit depth chart
    # if all basis_sets are the same.
    basis_sets = [result.basis_set for result in results]
    equivalent = "false"
    ground_truth, experiment_approx, experiment_truth, depths, min_energies = (0,)*5
    if basis_sets.count(basis_sets[0]) == len(basis_sets):
        # bond_distance = fci.get_minimum_distance("def2-QZVPPD")
        # FIXME bond_distance might not be available in the results. Hardcode 0.70 for now.
        bond_distance = 0.70
        ground_truth = fci.get_fci_value_by_dist("def2-QZVPPD", bond_distance)
        experiment_truth = fci.get_fci_value_by_dist(basis_sets[0], bond_distance)
        experiment_approx = hf.get_hf_value_by_dist(basis_sets[0], bond_distance)
        equivalent = "true"
        # For now we can assume that all runs have the same gate depths.
        depths = [result.get_runs()[0].gate_depth for result in results]
        # FIXME Different runs might have min_energy at different distances
        # and some might lack a value for the 'real' bond_distance
        min_energies = [result.min_energy for result in results]

    return Response(
        {
            "ids": ids,
            "names": names,
            "energies": energies,
            "distances": distances,
            "fci_distances": list(fci_distances),
            "fci_energies": list(fci_energies),
            "ground_truth": ground_truth,
            "experiment_truth": experiment_truth,
            "experiment_approx": experiment_approx,
            "depths": depths,
            "min_energies": min_energies,
            "equivalent": equivalent,
            "path_prefix": request.headers.get("SCRIPT_NAME", ""),
        },
        template_name="compare_detail.html"
    )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def leaderboard(request, *args, **kwargs):
    result_list = kwargs.get("result_list", None)
    criterion = kwargs.get("criterion", None)
    if criterion == "closest_minimum":
        list_name = "Closest minimum energy distances to \"FCI def2_QZVPPD\" minimum energt distances "
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
            "path_prefix": request.headers.get("SCRIPT_NAME", ""),
        },
        template_name="leaderboard.html",
    )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def invoke_leaderboard(request, criterion):

    if criterion == "closest_minimum":
        result_list = list(Result.objects.all())
        true_bond_distance = fci.get_minimum_distance("def2-QZVPPD")
        result_list.sort(key=lambda x: x.min_energy_distance-true_bond_distance)
    elif criterion == "smallest_variance":
        result_list = Result.objects.filter(include_in_variance=True).order_by("variance_from_fci")[:10]
    else:
        criterion = "min_energy"
        result_list = Result.objects.order_by("min_energy")[:10]

    return leaderboard(request._request, result_list=result_list, criterion=criterion)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_token(request):
    user = request.user
    token = Token.objects.get(user=user)
    return Response({'Token': f'{token}'}, status=status.HTTP_200_OK)
