# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from qleader.models import QResult
from qleader.serializers import QResultSerializer

@api_view(['GET', 'POST'])
def result_list(request):

    if request.method == 'GET':
        results = QResult.objects.all().order_by('created')
        serializer = QResultSerializer(results, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
