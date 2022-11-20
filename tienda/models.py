from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.


class Marca(models.Model):
    nombre = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    marca = models.ForeignKey('Marca', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=255)
    modelo = models.IntegerField(primary_key=True)
    unidades = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    detalles = models.TextField(blank=True, max_length=255)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    nombre = models.ForeignKey('Producto', on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.IntegerField()
    importe = models.FloatField()

    def __str__(self):
        return str(self.nombre)
