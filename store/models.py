from django.db import models
from django.db.models.base import Model

# Create your models here.


class usuario(models.Model):
    primer_nombre = models.CharField(max_length=120, blank=False)
    segundo_nombre = models.CharField(max_length=120, blank=True)
    primer_apellido = models.CharField(max_length=120, blank=False)
    segundo_apellido = models.CharField(max_length=120, blank=True)
    identificacion = models.IntegerField(max_length=13)
    correo = models.EmailField()
    celular = models.IntegerField(max_length=13)
    confirmado = models.BooleanField()
