from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ClienteRegistrationForm, UserRegistrationForm

# Create your views here.


def index(HttpResponse):
    return f'hello'


def register(request):
    if request.method == 'GET':
        user_registration_form = UserRegistrationForm()
        cliente_registration_form = ClienteRegistrationForm()
    else:
        user_registration_form = UserRegistrationForm(request.POST)
        cliente_registration_form = ClienteRegistrationForm(request.POST)
        print (cliente_registration_form.is_valid(), cliente_registration_form.errors, type(cliente_registration_form.errors))
        if user_registration_form.is_valid():
            user = user_registration_form.save()
            cliente_registration_form.instance.user = user
            print(cliente_registration_form.is_valid())
            
            if cliente_registration_form.is_valid():
                cliente = cliente_registration_form.save()
                return redirect('register_success')
    return render(request, 'store/register.html', {'cliente_form': cliente_registration_form,
                                                   'user_form' : user_registration_form})

def register_success(request):
    return render(request, 'store/register_success.html')