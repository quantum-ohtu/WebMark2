from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import Result
from qleader.helpers import create_runs, create_result
import json


@api_view(['GET', 'POST'])
def result_list(request):

    if request.method == 'GET':
        # results = Results.objects.all().order_by('created')
        return Response()
    elif request.method == 'POST':
        data_dict = json.loads(request.data)
        try:
            result = create_result(data_dict)
            result.save()
            runs_all = create_runs(data_dict, result)
            for run in runs_all:
                run.save()
            return Response('Success', status=status.HTTP_201_CREATED)
        except Exception as e:
            result.delete()
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


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
