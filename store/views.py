from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(HttpResponse):
    return f'hello'

def register(request):
    return render (request, 'store/register.html')