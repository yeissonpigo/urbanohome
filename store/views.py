from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ClienteRegistrationForm, UserRegistrationForm, Login
from django.contrib import messages
from django.contrib.auth import login as loginAuth, authenticate, logout as logoutAuth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password

# Create your views here.


def index(HttpResponse):
    return f'hello'


def login(request):
    if request.method == 'POST':
        form = Login(request = request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginAuth(request, user)
                messages.info(request, f"Bienvenido a nuestra tienda virtual, {username}")
                return redirect('register_success')
            else:
                messages.info(request, f"Usuario o contraseña incorrectos.")
        else:
            print(form.errors.as_text()) 
            messages.info(request, f"Usuario o contraseña incorrectos.")
    form = Login()
    return render(request, 'store/login.html', {'login_form': form})

def logout(request):
    logoutAuth(request)
    messages.info(request, 'Su sesión se ha cerrado correctamente.')
    return redirect('register_success')

def register(request):
    if request.method == 'GET':
        user_registration_form = UserRegistrationForm()
        cliente_registration_form = ClienteRegistrationForm()
    else:
        user_registration_form = UserRegistrationForm(request.POST)
        cliente_registration_form = ClienteRegistrationForm(request.POST)
        print(cliente_registration_form.is_valid(
        ), cliente_registration_form.errors, type(cliente_registration_form.errors))
        if user_registration_form.is_valid():
            user = user_registration_form.save(commit=False)
            user.password = make_password(user.password)
            user = user_registration_form.save()
            cliente_registration_form.instance.user = user
            print(cliente_registration_form.is_valid())

            if cliente_registration_form.is_valid():
                cliente = cliente_registration_form.save()
                return redirect('register_success')
    return render(request, 'store/register.html', {'cliente_form': cliente_registration_form,
                                                   'user_form': user_registration_form})


def register_success(request):
    return render(request, 'store/register_success.html')
