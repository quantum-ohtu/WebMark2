from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import QResult, QBatch
from qleader.helpers import extract_data
import json
import matplotlib.pyplot as plt
from PIL import Image


@api_view(['GET', 'POST'])
def result_list(request):

    if request.method == 'GET':
        # results = QResult.objects.all().order_by('created')
        return Response()
    elif request.method == 'POST':
        data_dict = json.loads(request.data)
        try:
            batch = QBatch()
            batch.save()
            ext_data = extract_data(data_dict, batch)
            for qresult in ext_data:
                qresult.save()
            return Response('Success', status=status.HTTP_201_CREATED)
        except Exception as e:
            batch.delete()
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def home(request):

    if request.method == 'GET':
        results = QResult.objects.all().order_by('created')
        # Here we can filter the list before displaying
        return Response({'results': results.values()},
                        template_name='home.html')


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def detail(request, batch_id):

    if request.method == 'GET':
        qresults_in_batch = QResult.objects.filter(batch_id=batch_id)

        distances = [result.distance for result in qresults_in_batch]
        energies = [result.energy for result in qresults_in_batch]

        return Response({'results':qresults_in_batch.values(),
                        'energies':energies,
                        'distances':distances,
                        'batch_id':batch_id},
                        template_name='detail.html')


def energy_distance_plot(qresults_in_batch):
    distances = [result.distance for result in qresults_in_batch]
    energies = [result.energy for result in qresults_in_batch]
    #plt.figure()
    plt.plot(distances, energies, label=qresults_in_batch[0].ansatz)
    plt.legend()
    # plt.show()
    plt.savefig("plot.png")
    return None
