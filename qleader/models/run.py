from django.db import models
import ast


class Run(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['created']

    def get_iteration_energies(self):
        return ast.literal_eval(self.energies)

    def __str__(self):
        return "Replace this"
