from hashlib import new
from wsgiref import validate
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from .forms import ClienteRegistrationForm, CreatePurchase, UserRegistrationForm, Login, CardForm, DeleteCardForm, CreatePurchase
from django.contrib import messages
from django.contrib.auth import login as loginAuth, authenticate, logout as logoutAuth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from .models import *
import json
import hashlib
from datetime import date
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def index(request):
    return render(request, 'store/home.html')

#Return gallery view
def gallery(request):
    gallery = Galeria.objects.all()
    return render(request, 'store/gallery.html', {'gallery': gallery},)

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
            messages.info(request, f"Usuario o contraseña incorrectos.")
    else:
        if request.user.is_authenticated:
            return HttpResponseForbidden('No tienes acceso a este método.')
    form = Login()
    return render(request, 'store/login.html', {'login_form': form})

# logout function takes care of login out the users
# request: Request object
# return redirect to a new page


def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
        logoutAuth(request)
        messages.info(request, 'Su sesión se ha cerrado correctamente.')
        return redirect('register_success')

# register function takes care of registering new users
# request: Request Object
# return if POST method, a new website, unless the info on the input is not valid
# return if GET method, website for register#


def register(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
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
                    cliente_registration_form.save()
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
    return render(request, 'store/store.html', {'products': products, })

# card function will check request method, if it's get, will show the form to save a new cart, if already exists doesn't do anything. If request is post, will save the cart if non existant on the database.
# request: Request Object
# return either a form to save data, or a json object for developing purposes.


def card(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
        if request.method == 'GET':
            card_form = CardForm()
        else:
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save(commit=False)
                my_card = Carro.objects.filter(
                    clienteId=card.clienteId, productoId=card.productoId)
                if my_card:
                    messages.error(
                        request, '¡Ups! Ya tienes este producto en tu carrito de compras. Para revisar tu carrito de compras, click AQUÍ.')
                else:
                    messages.success(
                        request, '¡Tu producto se ha añadido correctamente!')
                    card = card_form.save()
                data = send_message(messages.get_messages(request))
                return HttpResponse(json.dumps(data), content_type="application/json")
        return render(request, 'store/card_test.html', {'card_form': card_form, })

# card_index function will fetch all the objects from Carro table in database, but if request method is post, will update the card with the new quantity of products
# request: Request Object
#return a render of a new page, sending the carro info, or a json response to send confirmation of the request#


def card_index(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
        if request.method == 'GET':
            user = request.user.id
            my_cliente = Cliente.objects.get(user_id=request.user.id)
            my_cards = Carro.objects.filter(clienteId=my_cliente.id)
            my_productos = []
            for my_card in my_cards:
                my_product = Producto.objects.get(id=my_card.productoId.id)
                my_productos.append(my_product)
        else:
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save(commit=False)
                my_cart = Carro.objects.get(
                    clienteId=card.clienteId, productoId=card.productoId)
                if my_cart:
                    messages.success(
                        request, '¡Tu carro de compras se ha actualizado!')
                    my_cart.cantidad = card.cantidad
                    my_cart.save()
                else:
                    messages.success(
                        request, '¡Ups! Ha habido un error, intenta de nuevo.')

                data = send_message(messages.get_messages(request))
                return HttpResponse(json.dumps(data), content_type="application/json")
        return render(request, 'store/card.html', {'my_cards': my_cards, 'my_products': my_productos, 'userId': my_cliente.id, 'test': my_cliente
                                                   })

# delete_cart function will delete certain product from the cart. Is meant for ajax.
# request: Request object
# return json object with messages, and required data.


def delete_cart(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
        if request.method == 'POST':
            delete_form = DeleteCardForm(data=request.POST)
            if delete_form.is_valid():
                my_cart = Carro.objects.get(
                    clienteId=delete_form.instance.clienteId, productoId=delete_form.instance.productoId)
                deleted = my_cart.delete()
                if deleted[0] > 0:
                    messages.success(
                        request, 'El producto se ha eliminado de manera satisfactoria')
                else:
                    messages.error(
                        request, 'Lo sentimos, algo ha sucedido. Intenta nuevamente.')
            else:
                messages.error(
                    request, 'Lo sentimos, hubo un error, por favor intenta nuevamente más tarde.')
            data = send_message(messages.get_messages(request))
            return HttpResponse(json.dumps(data), content_type="application/json")


# send_message processes the data from messages to prepare it to be sent to ajax request.
# messages: messages type from django.
# return dictionary called data.
def send_message(messages):
    django_messages = []

    for message in messages:
        django_messages.append({
            "level": message.level,
            "message": message.message,
            "extra_tags": message.tags,
        })

    data = {}
    data['success'] = 'info'
    data['messages'] = django_messages

    return data

'''
checkout is going to take care of the resume of pedido. 
request: request del http
return render of checkout.html, with products variable.
'''

def checkout(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    elif request.method == 'GET':
        userId = request.user.id
        cliente = Cliente.objects.get(user_id = userId)
        total = get_total(cliente)

        #if the access to checkout is from profile, it means that venta doesn't need to be created.
        if request.GET['origin'] != '0':
            create_venta(userId, total, request)
        ventas = Venta.objects.get(clienteId = cliente.id)
        reference = generate_reference(ventas.referencia, total, 1)
        carros = Carro.objects.filter(clienteId = cliente)
        productos_to_send = []
        for carro in carros:
            producto = Producto.objects.get(id = carro.productoId.id)
            productos_to_send.append((producto, carro.cantidad))
        return render(request, 'store/checkout.html', {'products': productos_to_send, 'reference':ventas.referencia, 'reference_hash': reference})
    
def get_total(cliente):
    carros = Carro.objects.filter(clienteId = cliente)
    total = 0
    for carro in carros:
        producto =  carro.productoId
        total += producto.precio_venta * carro.cantidad
    return total

'''
generate_reference receives reference_code and total value, to generate a reference
for payu purposses
@reference_code: id of a venta object
@total: total amount to pay on the venta object
return reference value
'''
def generate_reference(reference_code, total, type, *args):
    apiKey = '4Vj8eK4rloUd272L48hsrarnUA'
    merchantId = '508029'
    currency = 'COP'
    if type == 1:
        #for dev mode change 508029 for the real merchanID and the first apiKey 
        raw_reference = f'{apiKey}~{merchantId}~{reference_code}~{total}~{currency}'
    elif type == 2:
        raw_reference = f'{apiKey}~{args[1].GET["merchantId"]}~{reference_code}~{total}~{args[1].GET["currency"]}~{args[0]}'
    reference = hashlib.md5(raw_reference.encode('utf-8')).hexdigest()
    return reference

'''
finish_purchase se encarga de crear la venta, la cual espera en futuros pasos cambiar su estado.
request: request object
return template
'''
def create_venta(user_id, total, request):
    cliente = Cliente.objects.get(user_id = user_id)
    
    venta = Venta(clienteId=cliente, fecha=date.today(), total=total, estadoId=Estado.objects.get(id=1), direccion='No aplica')
    carros = Carro.objects.filter(clienteId = cliente)
    total = get_total(cliente)
    new_pedido = 0
    
    venta.save()

    venta.referencia = 'urbho' + str(venta.id)
    venta.save()
    
    for carro in carros:
        producto = carro.productoId
        new_pedido = Pedido()
        new_pedido.precio_unidad = producto.precio_venta
        new_pedido.cantidad = carro.cantidad
        new_pedido.productoId = producto
        new_pedido.ventaId = venta
        new_pedido.save()
    
    return True
        
'''
delete_venta assure you to only have 1 venta and pedido per
user to avoid duplicates
@request Request object
return store view.
'''
def delete_venta(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
        if request.method == 'POST':
            cliente = Cliente.objects.get(user_id = request.user.id)
            my_venta = Venta.objects.get(clienteId = cliente.id, estadoId = 1)
            my_pedido = Pedido.objects.get(ventaId = my_venta)
            deleted = []
            deleted.append(my_pedido.delete())
            deleted.append(my_venta.delete())
            
            return ('Funciona')


'''
pay_response takes care of checking the integrity of the data sent by payU by checking the signature received from payU, with the data received from payU. If signature received is equal to signature calculated, then returns resume of payment. Otherwise, returns error.
@request: Request object
return: either resume of payment or error
'''

def pay_response(request):
    if request.method == 'GET':
        tx_value = calculate_tx_value(request.GET['TX_VALUE'])
        signature = generate_reference(request.GET['referenceCode'], tx_value, 2, request.GET['transactionState'], request)
        if signature == request.GET['signature']:
            #Start test. Delete on production
            cliente = Cliente.objects.get(user_id = request.user.id)
            venta = Venta.objects.get(clienteId = cliente)
            if request.GET['polResponseCode'] == '1':
                venta.estadoId = Estado.objects.get(id = 2)
                send_mail(
                    subject='Nuevo pago confirmado',
                    message=f'El pago de la venta id {venta.id}, realizada por el cliente {cliente} se ha confirmado correctamente. Por favor, encargarse del envío de los productos',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                    )
            elif request.GET['polResponseCode'] == '4':
                venta.estadoId = Estado.objects.get(id = 3)
            else:
                venta.estadoId = Estado.objects.get(id = 4)
            venta.save()
            #End test.
            return render(request, 'store/payu_resume.html', {'data': request.GET, 'tx_value': tx_value, 'signature': signature})
        else:
            messages.error(request, 'Lo sentimos, los datos se han visto comprometidos.')
            return redirect('checkout')


'''
pay_response takes care of checking the integrity of the data sent by payU by checking the signature received from payU, with the data received from payU. If signature received is equal to signature calculated, then returns resume of payment. Otherwise, returns error.
@request: Request object
return: either 200 code or error code
'''
def pay_confirmation(request):
    if request.method == 'POST':
        tx_value = calculate_tx_value(request.GET['TX_VALUE'])
        signature = generate_reference(request.GET['referenceCode'], tx_value, 2, request.GET['transactionState'], request)
        if signature == request.GET['signature']:
            cliente = Cliente.objects.get(user_id = request.user.id)
            venta = Venta.objects.get(clienteId = cliente)
            if request.POST['state_pol'] == 1:
                venta.estadoId = Estado.objects.get(id = 2)
                send_mail(
                    subject='Nuevo pago confirmado',
                    message=f'El pago de la venta id {venta.id}, realizada por el cliente {cliente} se ha confirmado correctamente. Por favor, encargarse del envío de los productos',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                    )

            elif request.POST['state_pol'] == 4:
                venta.estadoId = Estado.objects.get(id = 3)

            else:
                venta.estadoId = Estado.objects.get(id = 4)

            venta.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

#calculate_tx_value takes care of rounding tx_value sent from payU to 1 digit after comma.
#@tx_value:tx_value received from payU
#return: return rounded tx_value
def calculate_tx_value(tx_value):
    final_tx_value = str("{:.1f}".format(round(float(tx_value))))
    return final_tx_value

#profile returns all the ventas that certaing logged in user has generated.
#@request: request info
#return: render profile html
def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
        if request.method == 'GET':
            cliente = Cliente.objects.get(user_id=request.user.id)
            ventas = Venta.objects.filter(clienteId = cliente)
            return render(request, 'store/profile.html', {'ventas':ventas})

def products(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes acceso a este método.')
    else:
        if request.method == 'GET':
            my_cliente = Cliente.objects.get(user_id=request.user.id)
            my_cards = Pedido.objects.filter(ventaId=request.GET['ventaId'])
            my_productos = []
            for my_card in my_cards:
                my_product = Producto.objects.get(id=my_card.productoId.id)
                my_productos.append(my_product)
        return render(request, 'store/card.html', {'my_cards': my_cards, 'my_products': my_productos, 'userId': my_cliente.id, 'test': my_cliente, 'origin': request.GET['origin']
                                                   })