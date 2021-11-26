from django import forms
from django.db.models import fields
from .models import Cliente, User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirmar contraseña'}))
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        
class ClienteRegistrationForm(forms.ModelForm):
    identificacion = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Identificación'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Correo'}))
    celular = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Identificación'}))
    class Meta:
        model = Cliente
        
        fields = ['identificacion', 'correo', 'celular']