from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect

from .models import Producto, Compra
from .forms import ProductoForm, CheckOutForm


# Create your views here.


def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/listado.html', {'productos': productos})


def nuevo_producto(request):
    producto = {}
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
    producto['form'] = form
    return render(request, 'tienda/nuevo_producto.html', producto)


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listado')
    form = {'form': form}
    return render(request, 'tienda/editar_producto.html', form)


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listado')
    return render(request, 'tienda/eliminar.html', {'producto': producto})


def listado_compra(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/listado_compra.html', {'productos': productos})


def checkout(request, pk):
    form = CheckOutForm()
    producto = Producto.objects.all()
    p = get_object_or_404(Producto, pk=pk)
    valida_p = True
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            unidades = form.cleaned_data['unidades']
            if unidades > p.unidades:
                valida_p = False
            else:
                p.unidades = p.unidades - unidades
                p.save()
#                Compra.objects.create(nombre=p.nombre, fecha=timezone.now(), unidades=p.unidades, importe=p.precio)
                return redirect('listado_compra')
    else:
        return render(request, 'tienda/compra.html', {'form': form, 'producto': p, 'pk': pk})
