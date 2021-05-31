from django.db import models
from jsonfield import JSONField
# import tequila as tq


class QResult(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    result = JSONField()   # Default parameters for the time!!!
