from this import d
from django import template

register = template.Library()

@register.filter
def find_id(productos, id):
    new_productos = [producto for producto in productos if producto.id == id]
    return new_productos