from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect

from .models import Producto, Compra, Marca
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
        messages.add_message(request, messages.INFO, "Registro creado")
    producto['form'] = form
    return render(request, 'tienda/nuevo_producto.html', producto)


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Registro editado")
            return redirect('listado')
    form = {'form': form}
    return render(request, 'tienda/editar_producto.html', form)


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.add_message(request, messages.INFO, "Producto eliminado correctamente")
        return redirect('listado')
    return render(request, 'tienda/eliminar.html', {'producto': producto})


def listado_compra(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/listado_compra.html', {'productos': productos})


@transaction.atomic
def checkout(request, pk):
    form = CheckOutForm()
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            unidades = form.cleaned_data['unidades']
            if request.user.is_authenticated:
                user = request.user.id
            else:
                user = None
            producto.unidades = producto.unidades - unidades
            producto.save()
            Compra.objects.create(usuario_id=user, nombre=producto, fecha=timezone.now(), unidades=unidades,
                                  importe=producto.precio * unidades)
            messages.add_message(request, messages.INFO, "Compra realizada")
            return redirect('listado_compra')
    else:
        return render(request, 'tienda/compra.html', {'form': form, 'producto': producto, 'pk': pk})


def registrar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            us = form.save()
            login(request, us)
            messages.add_message(request, messages.INFO, "Registro exitoso")
            return redirect('welcome')
        else:
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
                messages.add_message(request, messages.INFO, f"Has iniciado sesión como {username}")
                return redirect('welcome')
            else:
                messages.error(request, f"Invalid username or password")
        else:
            messages.error(request, f"Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'tienda/iniciar_sesion.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    messages.add_message(request, messages.INFO, f"Has cerrado sesión")
    return redirect('welcome')


def informes(request):
    return render(request, 'tienda/informes.html')


def informe_marcas(request):
    marcas = Marca.objects.all().values()
    return render(request, 'tienda/listado_informes.html', {'marcas': marcas})


def marcas_productos(request, nombre):
    listado_productos = Producto.objects.filter(marca__nombre__icontains=nombre).values()
    return render(request, 'tienda/informe_producto.html', {'listado_productos': listado_productos})


def top_ten_productos(request):
    id_producto = Producto.objects.all()
    productos = Compra.objects.values('nombre__nombre').annotate(u_vendidas=Sum('unidades')).order_by('-u_vendidas')[:10]
    return render(request, 'tienda/top_productos.html', {'productos': productos, 'id_producto': id_producto})


def lista_usuarios(request):
    usuario = User.objects.all().values()
    return render(request, 'tienda/lista_usuarios.html', {'usuarios': usuario})


def compras_usuarios(request, usuario):
    productos = Compra.objects.filter(usuario=usuario)
    usuarios = User.objects.values('username').filter(id=usuario)
    return render(request, 'tienda/compras_usuario.html', {'productos': productos, 'usuarios': usuarios})


def top_ten_usuarios(request):
    usuarios = User.objects.values('username').annotate(total_compras=Sum('compra__importe')).order_by('-total_compras')[:10]
    return render(request, 'tienda/top_usuarios.html', {'usuarios': usuarios})
