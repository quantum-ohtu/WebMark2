from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import Run
from qleader.helpers import create_results, create_run
import json


@api_view(['GET', 'POST'])
def result_list(request):

    if request.method == 'GET':
        # results = Results.objects.all().order_by('created')
        return Response()
    elif request.method == 'POST':
        data_dict = json.loads(request.data)
        try:
            run = create_run(data_dict)
            run.save()
            Results_all = create_results(data_dict, run)
            for Results in Results_all:
                Results.save()
            return Response('Success', status=status.HTTP_201_CREATED)
        except Exception as e:
            run.delete()
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def home(request):

    if request.method == 'GET':
        runs = Run.objects.all().order_by('created')
        # Here we can filter the list before displaying
        return Response({'runs': runs.values(),
                        'path_prefix': request.headers.get('PathPrefix', '')},
                        template_name='home.html')


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def detail(request, run_id):

    if request.method == 'GET':
        run = Run.objects.filter(id=run_id)[0]
        results_all = run.results.all()

        distances = [results.distance for results in results_all]
        energies = [results.energy for results in results_all]
        iteration_energies = [results.get_iteration_energies() for results in results_all]

        name = ' '.join([run.basis_set, run.transformation])

        return Response({'run': run,
                         'results_all': results_all,
                         'name': name,
                         'energies': energies,
                         'distances': distances,
                         'iterationEnergies': iteration_energies,
                         'path_prefix': request.headers.get('PathPrefix', '')},
                        template_name='detail.html')
