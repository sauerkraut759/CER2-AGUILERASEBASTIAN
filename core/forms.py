from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioSistema, SolicitudRetiro

class UsuarioSistemaForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

        self.fields['password1'].help_text = 'Mínimo 8 carácteres, use letras y números.'

    first_name = forms.CharField(max_length=50, label="Nombre")
    last_name = forms.CharField(max_length=50, label="Apellido")
    telefono = forms.CharField(max_length=9, label="Télefono", widget = forms.TextInput(attrs={'placeholder': 'Ej: 9 1234 5678'}))
    direccion = forms.CharField(max_length=100, label="Dirreción")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        help_texts = {
            'username': 'Debe contener solo letras y números',
        }

class SolicitudRetiroForm(forms.ModelForm):
    class Meta:
        model = SolicitudRetiro
        fields = ['material', 'cantidad', 'unidad', 'fecha_estimada']
        labels = {
            'material': 'Tipo de material reciclable',
            'cantidad': 'Cantidad estimada',
            'unidad': 'Unidad de medida',
            'fecha_estimada': 'Fecha estimada de retiro'
        }
        widgets = {
            'material': forms.Select(attrs={'class':'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Ej: 2.5'}),
            'unidad': forms.Select(attrs={'class':'form-control'}),
            'fecha_estimada': forms.DateInput(attrs = {'type': 'date', 'class':'form-control'})
        }