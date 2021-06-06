from django.db import models
from django.db.models.fields import CharField, TextField
from jsonfield import JSONField
# import tequila as tq


class QResult(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    result = JSONField()   # Default parameters for the time!!!
    hamiltonian = TextField()
    ansatz = TextField()
    optimizer = CharField(max_length=50)

    def __str__(self):
        return "Replace this"
