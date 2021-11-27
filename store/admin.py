from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Cliente),
admin.site.register(TipoIdentificacion)
admin.site.register(TipoProducto)
admin.site.register(Color)
admin.site.register(Producto)