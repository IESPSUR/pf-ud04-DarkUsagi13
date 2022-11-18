from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Producto, Marca


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"


class CheckOutForm(forms.Form):
    unidades = forms.FloatField(label='Unidades')


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('marca',)
