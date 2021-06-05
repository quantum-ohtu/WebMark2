from rest_framework import serializers
from qleader.models import QResult


class QResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QResult
        fields = ['created', 'result', 'hamiltonian', 'ansatz', 'optimizer']
