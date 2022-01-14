from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ClienteRegistrationForm, UserRegistrationForm, Login, CardForm
from django.contrib import messages
from django.contrib.auth import login as loginAuth, authenticate, logout as logoutAuth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from .models import Producto, User, Cliente, Carro
import json

# Create your views here.


def index(HttpResponse):
    return f'hello'

# Login function takes care of user's login.
# request: Request object
# return a message of success with a redirect to a new page
# Or
# Return login website again with a failure message


def login(request):
    if request.method == 'POST':
        form = Login(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginAuth(request, user)
                messages.info(
                    request, f"Bienvenido a nuestra tienda virtual, {username}")
                return redirect('register_success')
            else:
                messages.info(request, f"Usuario o contraseña incorrectos.")
        else:
            print(form.errors.as_text())
            messages.info(request, f"Usuario o contraseña incorrectos.")
    form = Login()
    return render(request, 'store/login.html', {'login_form': form})

# logout function takes care of login out the users
# request: Request object
# return redirect to a new page


def logout(request):
    logoutAuth(request)
    messages.info(request, 'Su sesión se ha cerrado correctamente.')
    return redirect('register_success')

# register function takes care of registering new users
# request: Request Object
# return if POST method, a new website, unless the info on the input is not valid
# return if GET method, website for register#


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

# register_success function is mainly a testing function, users will be redirected here when registering, or login
# request: Request Object
# return new page
# #


def register_success(request):
    return render(request, 'store/register_success.html')

# show_items function will fetch all the product from the database
# request: Request Object
#return a render of a new page, sending the products info#


def show_items(request):
    products = Producto.objects.all()
    if request.user.is_authenticated:
        username = request.user
        user = Cliente.objects.get(user=username.id)
        return render(request, 'store/store.html', {'products': products, 'userId': user.id})
    return render(request, 'store/store.html', {'products': products,})

# card function will check request method, if it's get, will show the form to save a new cart, if already exists doesn't do anything. If request is post, will save the cart if non existant on the database.
# request: Request Object
# return either a form to save data, or a json object for developing purposes.


def card(request):
    if request.method == 'GET':
        card_form = CardForm()
    else:
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            test = {
                "test": "This is a test"
            }
            my_card = Carro.objects.filter(clienteId=card.clienteId, productoId=card.productoId)
            if my_card:
                messages.error(request, '¡Ups! Ya tienes este producto en tu carrito de compras. Para revisar tu carrito de compras, click AQUÍ.')
            else:
                messages.success(request, '¡Tu producto se ha añadido correctamente!')
                card = card_form.save()
            django_messages = []

            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
            })
                
            data = {}
            data['success'] = 'i dont know'
            data['messages'] = django_messages
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'store/card_test.html', {'card_form': card_form, })

# card_index function will fetch all the objects from Carro table in database
# request: Request Object
#return a render of a new page, sending the carro info#


def  card_index(request):
    if request.method == 'GET':
        my_cliente = Cliente.objects.get(user_id = request.user.id)
        my_cards = Carro.objects.filter(clienteId = my_cliente.id)
        my_productos = []
        for my_card in my_cards:
            my_product = Producto.objects.get(id = my_card.productoId.id)
            my_productos.append(my_product)
    return render(request, 'store/card.html', {'my_cards': my_cards, 'my_products': my_productos
    })