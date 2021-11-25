from django.shortcuts import render
from django.http import HttpResponse
from .forms import ClienteRegistrationForm, UserRegistrationForm

# Create your views here.


def index(HttpResponse):
    return f'hello'


def register(request):
    user_registration_form = UserRegistrationForm()
    cliente_registration_form = ClienteRegistrationForm()
    return render(request, 'store/register.html', {'cliente_form': cliente_registration_form,
                                                   'user_form' : user_registration_form})
