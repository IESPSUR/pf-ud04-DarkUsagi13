from django import forms
from .models import Producto, Marca


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
