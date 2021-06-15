from django.db import models
from django.db.models.fields import CharField, TextField, FloatField, SmallIntegerField
# from jsonfield import JSONField
# import tequila as tq


class QResult(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    energy = FloatField(default=None)
    optimizer = CharField(default="", max_length=50)
    tqversion = TextField(default="")
    variables = TextField(default="")
    history_energies = TextField(default="")
    gradients = TextField(default="")
    angles = TextField(default="")
    energies_calls = TextField(default="")
    gradients_calls = TextField(default="")
    angles_calls = TextField(default="")
    final_simplex = TextField(default="")
    fun = FloatField(default=None)
    message = TextField(default="")
    nfev = SmallIntegerField(default=None)
    nit = SmallIntegerField(default=None)
    status = SmallIntegerField(default=None)
    success = CharField(default="", max_length=20)
    x = TextField(default="")
    hamiltonian = TextField(default="")
    ansatz = TextField(default="")
    molecule = TextField(default="")
    distance = FloatField(default=None)

    def __str__(self):
        return "Replace this"
