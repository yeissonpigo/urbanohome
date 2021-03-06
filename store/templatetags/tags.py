from this import d
from django import template

register = template.Library()

@register.filter
def find_name(productos, id):
    new_productos = [producto for producto in productos if producto.id == id]
    return new_productos[0]

@register.filter
def find_id(productos, id):
    new_productos = [producto for producto in productos if producto.id == id]
    return new_productos[0].id

@register.filter
def precio_venta(producto):
    return producto.precio_venta

@register.filter
def image(producto):
    return producto.imagen.url

@register.filter
def total(productos):
    total = 0
    for producto in productos:
        total += producto.precio_venta
    return total

@register.filter
def calcular_total(pedido):
    total = pedido[0].precio_venta * pedido[1]
    return total

@register.filter
def calcular_suma(pedidos):
    total = 0
    for pedido in pedidos:
        total += pedido[0].precio_venta * pedido[1]
    return total