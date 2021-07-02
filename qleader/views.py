from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import Result
from qleader.helpers import populate_result
import json


@api_view(['GET', 'POST'])
def result_list(request):

    if request.method == 'GET':
        # results = Results.objects.all().order_by('created')
        return Response()
    elif request.method == 'POST':
        data_dict = json.loads(request.data)
        error = populate_result(data_dict)
        if error == "NoErr":
            return Response('Success', status=status.HTTP_201_CREATED)
        else:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def home(request):

    if request.method == 'GET':
        runs = Result.objects.all().order_by('created')
        # Here we can filter the list before displaying
        return Response({'runs': runs.values(),
                        'path_prefix': request.headers.get('PathPrefix', '')},
                        template_name='home.html')


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def detail(request, result_id):

    if request.method == 'GET':
        result = Result.objects.filter(id=result_id)[0]
        runs_all = result.runs.all()

        distances = [results.distance for results in runs_all]
        energies = [results.energy for results in runs_all]
        iteration_energies = [results.get_iteration_energies() for results in runs_all]

        name = ' '.join([result.basis_set, result.transformation])

        return Response({'result': result,
                         'runs_all': runs_all,
                         'name': name,
                         'energies': energies,
                         'distances': distances,
                         'iterationEnergies': iteration_energies,
                         'path_prefix': request.headers.get('PathPrefix', '')},
                        template_name='detail.html')


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def leaderboard(request, *args, **kwargs):
    result_list = kwargs.get('result_list', None)
    criterion = kwargs.get('criterion', None)
    if criterion == "closest_minimum":
        list_name = "Top 10 closest minimum to \"gold standard\""
    elif criterion == "smallest_variance":
        list_name = "Top 10 smallest variance to \"gold standard\""
    elif not criterion:
        return redirect('/')
    else:
        list_name = "Top 10 minimum energy"
    return Response({'results': result_list, 'list_name': list_name}, template_name='leaderboard.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def invoke_leaderboard(request, criterion):

    if criterion == "closest_minimum":
        result_list = [{'id': "This leaderboard category is not yet implemented"}]
    elif criterion == "smallest_variance":
        result_list = [{'id': "This leaderboard category is not yet implemented"}]
    else:
        criterion = "min_energy"
        result_list = Result.objects.order_by("min_energy")[:10]

    return leaderboard(request._request, result_list=result_list, criterion=criterion)