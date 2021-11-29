from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL

# Create your models here.

class Ciudad(models.Model):
    nombre = models.CharField(max_length=40)
    
    def __str__(self):
        return f'{self.nombre}'

class Direccion(models.Model):
    direccion = models.TextField()
    ciudadId = models.ForeignKey(Ciudad, on_delete=PROTECT)
    
    def __str__(self):
        return f'{self.direccion}'

class TipoIdentificacion(models.Model):
    nombre = models.CharField(max_length=15)
    
    def __str__(self):
        return f'{self.nombre}'
  
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    identificacionId = models.ForeignKey(TipoIdentificacion, on_delete=PROTECT)
    identificacion = models.IntegerField()
    correo = models.EmailField()
    celular = models.BigIntegerField()
    confirmado = models.BooleanField(default=False)
    direccionId = models.ForeignKey(Direccion, on_delete=SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.user.username}'

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    
    def __str__(self):
        return f'{self.nombre}'
    
class Color(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.nombre}'
    
class Producto (models.Model):
    nombre = models.CharField(max_length=30)
    precio_compra = models.FloatField()
    precio_venta = models.FloatField()
    stock = models.IntegerField()
    tipoProductoId = models.ForeignKey(TipoProducto, on_delete=PROTECT)
    colorId = models.ForeignKey(Color, on_delete=PROTECT)
    imagen = models.FileField(upload_to='media/')
    
    def __str__(self):
        return f'{self.nombre}'