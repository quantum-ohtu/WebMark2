from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, TextField, FloatField, SmallIntegerField
import ast


class Result(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    optimizer = CharField(default="", max_length=50)
    tqversion = TextField(default="")
    basis_set = CharField(default="", max_length=50)
    transformation = CharField(default="", max_length=50)
    min_energy = FloatField(default=float("inf"))

    def __str__(self):
        return "Replace this"


class Run(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(Result, related_name='runs', on_delete=CASCADE)
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
    jac = TextField(default="", blank=True)
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

    class Meta:
        ordering = ['created']

    def get_iteration_energies(self):
        return ast.literal_eval(self.energies)

    def __str__(self):
        return "Replace this"
