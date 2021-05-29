from django.db import models
# import tequila as tq


class QResult(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    result = models.JSONField()   # Default parameters for the time!!!
