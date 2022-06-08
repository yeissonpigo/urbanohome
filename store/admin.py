from django.contrib import admin

from store.views import card
from .models import *
# Register your models here.

class VentaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cliente','fecha', 'total', 'estadoId', 'direccion', 'referencia',) 

    def cliente(self, obj):
        cliente = Cliente.objects.get(id=obj.clienteId.id)
        return cliente

admin.site.register(Cliente),
admin.site.register(TipoIdentificacion)
admin.site.register(TipoProducto)
admin.site.register(Color)
admin.site.register(Producto)
admin.site.register(Carro)
admin.site.register(Direccion)
admin.site.register(Ciudad)
admin.site.register(Estado)
admin.site.register(Venta, VentaAdmin)
admin.site.register(Pedido)
admin.site.register(Galeria)