from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/listado/', views.listado, name='listado'),
    path('tienda/admin/nuevo_producto/', views.nuevo_producto, name='nuevo_producto'),
    path('tienda/admin/editar_producto/<int:pk>', views.editar_producto, name='editar_producto'),
    path('tienda/admin/eliminar_producto/<int:pk>', views.eliminar_producto, name='eliminar_producto'),
    path('tienda/listado_compra/', views.listado_compra, name='listado_compra'),
    path('tienda/checkout/<int:pk>s', views.checkout, name='checkout')
]
