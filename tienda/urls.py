from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('listado/', views.listado, name='listado'),
    path('nuevo_prducto/', views.nuevo_producto, name='nuevo_producto'),
    path('editar_producto/<int:pk>', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>', views.eliminar_producto, name='eliminar_producto'),
]
