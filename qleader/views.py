# from django.shortcuts import render
from rest_framework import viewsets
from qleader.models import QResult
from qleader.serializers import QResultSerializer


class QResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows results to be viewed or edited.
    """
    queryset = QResult.objects.all().order_by('created')
    serializer_class = QResultSerializer
