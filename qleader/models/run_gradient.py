from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField, FloatField
from qleader.models.run import Run
from .result import Result


# An abstract class for scipy based
class RunGradient(Run):
    distance = FloatField(default=None)
    energy = FloatField(default=None)
    variables = TextField(default="")
    energies = TextField(default="")
    gradients = TextField(default="")
    angles = TextField(default="")
    energies_calls = TextField(default="")
    gradients_calls = TextField(default="")
    angles_calls = TextField(default="")
    hamiltonian = TextField(default="")
    ansatz = TextField(default="")
    molecule = TextField(default="")

    class Meta:
        abstract = True


# "Nesterov" optimizer
class RunGradientNesterov(RunGradient):
    result = models.ForeignKey(
        Result, related_name='runs_nesterov', on_delete=CASCADE
    )
    moments = TextField(default="", blank=True)
