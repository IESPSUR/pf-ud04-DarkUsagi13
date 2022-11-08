from django import forms
from .models import Producto, Marca


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "marca",
            "modelo",
            "nombre",
            "unidades",
            "precio",
            "detalles",
        ]


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = [
            "nombre",
        ]
