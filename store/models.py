from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.


class cliente(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    primer_nombre = models.CharField(max_length=120, blank=False)
    segundo_nombre = models.CharField(max_length=120, blank=True)
    primer_apellido = models.CharField(max_length=120, blank=False)
    segundo_apellido = models.CharField(max_length=120, blank=True)
    identificacion = models.IntegerField(max_length=13)
    correo = models.EmailField()
    celular = models.IntegerField(max_length=13)
    confirmado = models.BooleanField()
