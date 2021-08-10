from django.db import models
from django.db.models.fields import BooleanField, CharField, SmallIntegerField, TextField, FloatField
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from qleader.models.optimizers import gradient_optimizers
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    real_name = models.CharField(max_length=30, blank=True)
    institution = models.CharField(max_length=30, default="default") # blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
