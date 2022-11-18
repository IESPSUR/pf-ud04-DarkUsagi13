from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
            if request.user.is_authenticated:
                user = request.user.id
            else:
                user = None
            if unidades > p.unidades:
                valida_p = False
            else:
                p.unidades = p.unidades - unidades
                p.save()
                Compra.objects.create(usuario_id=user, nombre=p, fecha=timezone.now(), unidades=unidades, importe=p.precio * unidades)
                return redirect('listado_compra')
    else:
        return render(request, 'tienda/compra.html', {'form': form, 'producto': p, 'pk': pk})


def registrar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            us = form.save()
            login(request, us)
            messages.add_message(request, messages.INFO, "Registro exitoso")
            return redirect('welcome')
        messages.error(request, "Registro no válido")
    form = UserCreationForm()
    return render(request, "tienda/registro.html", {"form": form})


def inicio_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('welcome')
            else:
                messages.error(request, f"Invalid username or password")
        else:
            messages.error(request, f"Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'tienda/iniciar_sesion.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('welcome')
