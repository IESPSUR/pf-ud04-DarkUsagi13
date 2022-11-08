from django.shortcuts import render
from .models import Producto
from .forms import ProductoForm
# Create your views here.


def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/listado.html', {'productos': productos})


def NuevoProducto(request):
    context = {}
    form = ProductoForm(request.POST)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'tienda/nuevoproducto.html', context)


