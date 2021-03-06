from django import forms
from django.db import models
from django.db.models import fields
from .models import Cliente, User, TipoIdentificacion, Carro, Pedido, Venta
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirmar contraseña'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombres reales'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellidos reales'}))
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
        
    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )
        
class ClienteRegistrationForm(forms.ModelForm):
    identificacion = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Identificación'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Correo'}))
    celular = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Celular'}))
    class Meta:
        model = Cliente
        
        fields = ['correo', 'celular', 'identificacionId',  'identificacion']
        
    def __init__(self, *args, **kwargs):
        super(ClienteRegistrationForm, self).__init__(*args, **kwargs)
        # this is pseudo code but you should get all options
        # then get the product related to each variant
        options = TipoIdentificacion.objects.all()
        ids = [(i.id, i.nombre) for i in options]
        self.fields['identificacionId'].choices = ids
        
class Login(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
class CardForm(forms.ModelForm):
    
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Cantidad'}))
    
    class Meta:
        model = Carro
        fields = ('clienteId', 'productoId', 'cantidad')
        
class DeleteCardForm(forms.ModelForm):
    
    class Meta:
        model = Carro
        fields = ('clienteId', 'productoId')
        
class CreatePurchase(forms.ModelForm):
    
    class Meta:
        model = Venta
        fields = ('direccion',)