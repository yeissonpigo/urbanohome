from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT

# Create your models here.

class Ciudad(models.Model):
    nombre = models.CharField(max_length=40)

class Direccion(models.Model):
    direccion = models.TextField()
    ciudadId = models.ForeignKey(Ciudad, on_delete=PROTECT)

class TipoIdentificacion(models.Model):
  nombre = models.CharField(max_length=15)
  
class cliente(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    primer_nombre = models.CharField(max_length=120, blank=False)
    segundo_nombre = models.CharField(max_length=120, blank=True)
    primer_apellido = models.CharField(max_length=120, blank=False)
    segundo_apellido = models.CharField(max_length=120, blank=True)
    identificacionId = models.ForeignKey(TipoIdentificacion, on_delete=PROTECT)
    identificacion = models.IntegerField(max_length=13)
    correo = models.EmailField()
    celular = models.IntegerField(max_length=13)
    confirmado = models.BooleanField()
