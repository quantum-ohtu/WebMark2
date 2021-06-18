from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, TextField, FloatField, SmallIntegerField
# from jsonfield import JSONField
# import tequila as tq


class QBatch(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    optimizer = CharField(default="", max_length=50)
    tqversion = TextField(default="")
    basis_set = CharField(default="", max_length=50)
    transformation = CharField(default="", max_length=50)

    def __str__(self):
        return "Replace this"


class QResult(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    batch = models.ForeignKey(QBatch, on_delete=CASCADE)
    energy = FloatField(default=None)
    variables = TextField(default="")
    energies = TextField(default="")
    gradients = TextField(default="")
    angles = TextField(default="")
    energies_calls = TextField(default="")
    gradients_calls = TextField(default="")
    angles_calls = TextField(default="")
    energy_evaluations = TextField(default="")
    angles_evaluations = TextField(default="")
    gradients_evaluations = TextField(default="")
<<<<<<< HEAD
    jac = TextField(default="", blank=True)
=======
    jac = TextField(default="", blank=True,)
>>>>>>> 1b3fd0330b259ba22cf70d93e2ebd9e8095b55a1
    hess_inv = TextField(default="", blank=True)
    hessians = TextField(default="", blank=True)
    final_simplex = TextField(default="")
    fun = FloatField(default=None)
    message = TextField(default="")
    nfev = SmallIntegerField(default=None, blank=True, null=True)
    nit = SmallIntegerField(default=None)
    njev = SmallIntegerField(default=None, blank=True, null=True)
    status = SmallIntegerField(default=None)
    success = CharField(default="", max_length=20)
    x = TextField(default="")
    hamiltonian = TextField(default="")
    ansatz = TextField(default="")
    molecule = TextField(default="")
    distance = FloatField(default=None)

    def __str__(self):
        return "Replace this"
