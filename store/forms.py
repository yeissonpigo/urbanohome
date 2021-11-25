from django import forms
from django.db.models import fields
from .models import Cliente, User

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
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
    class Meta:
        model = Cliente
        
        fields = ['identificacion', 'correo', 'celular']