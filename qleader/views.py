from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import QResult
from qleader.serializers import QResultSerializer
from qleader.helpers import extract_data
import json


@api_view(['GET', 'POST'])
def result_list(request):

    if request.method == 'GET':
        results = QResult.objects.all().order_by('created')
        serializer = QResultSerializer(results, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data_dict = json.loads(request.data)
        ext_data = extract_data(data_dict)
        for entry in ext_data:
            serializer = QResultSerializer(data=entry)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def home(request):

    if request.method == 'GET':
        results = QResult.objects.all().order_by('created')
        # Here we can filter the list before displaying
        return Response(
            {'results': results.values()},
            template_name='home.html'
        )
