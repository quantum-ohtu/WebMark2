from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from qleader.models.run import Run
from .result import Result


class RunGradient(Run):
    result = models.ForeignKey(
        Result, related_name='runs_gradient', on_delete=CASCADE
    )
    moments = TextField(default="", blank=True)
<<<<<<< HEAD
    qubits = SmallIntegerField(default=0)
    gate_depth = SmallIntegerField(default=0)
=======
>>>>>>> 9057f5013184f68f863edfdc6a4b1a6ee8e7438c
