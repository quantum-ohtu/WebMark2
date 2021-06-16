from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import QResult, QBatch
from qleader.helpers import extract_data
import json


@api_view(['GET', 'POST'])
def result_list(request):

    if request.method == 'GET':
        results = QResult.objects.all().order_by('created')
        return Response(results)
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
        print(results.values())
        # Here we can filter the list before displaying
        return Response(
            {'results': results.values()},
            template_name='home.html'
        )
