from django.db import models
from django.db.models.fields import CharField, TextField, FloatField


class Result(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    optimizer = CharField(default="", max_length=50)
    tqversion = TextField(default="")
    basis_set = CharField(default="", max_length=50)
    transformation = CharField(default="", max_length=50)
    min_energy = FloatField(default=float("inf"))
    min_energy_distance = FloatField(default=float("inf"))
    min_delta = FloatField(default=float("inf"))
    min_delta_distance = FloatField(default=float("inf"))

    def __str__(self):
        return "Replace this"
