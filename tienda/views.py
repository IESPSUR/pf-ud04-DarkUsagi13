from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm
# Create your views here.


def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/listado.html', {'productos': productos})


def nuevo_producto(request):
    producto = {}
    form = ProductoForm(request.POST)
    if form.is_valid():
        form.save()
    producto['form'] = form
    return render(request, 'tienda/nuevo_producto.html', producto)


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.nombre = form.cleaned_data['nombre']
            form.modelo = form.cleaned_data['modelo']
            form.unidades = form.cleaned_data['unidades']
            form.precio = form.cleaned_data['precio']
            form.detalles = form.cleaned_data['detalles']
            form.marca = form.cleaned_data['marca']
            form.save()
        else:
            print('Formulario no válido')
    return render(request, 'tienda/nuevo_producto.html', {'form': form})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listado')
    return render(request, 'tienda/eliminar.html', {'producto': producto})
