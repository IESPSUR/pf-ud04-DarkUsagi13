from django.db import models
from django.conf import settings

# Create your models here.


class Marca(models.Model):
    nombre = models.CharField(max_length=255, primary_key=True)


class Product(models.Model):
    modelo = models.ForeignKey('Marca', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    unidades = models.IntegerField(default=1)
    precio = models.FloatField(default=0)
    detalles = models.TextField(blank=True, max_length=255)
