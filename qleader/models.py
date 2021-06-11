from django.db import models
from django.db.models.fields import CharField, TextField
# from jsonfield import JSONField
# import tequila as tq


class QResult(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    energies = TextField(default="")
    variables = TextField(default="")
    histories = TextField(default="")
    scipy_results = TextField(default="")
    hamiltonian = TextField(default="")
    ansatz = TextField(default="")
    molecule = TextField(default="")
    optimizer = CharField(default="", max_length=50)
    tqversion = TextField(default="")

    def __str__(self):
        return "Replace this"
