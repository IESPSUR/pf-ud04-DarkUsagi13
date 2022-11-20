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
    path('tienda/checkout/<int:pk>', views.checkout, name='checkout'),
    path('tienda/registrar_usario', views.registrar_usuario, name='registrar_usuario'),
    path('tienda/iniciar_sesion', views.inicio_sesion, name='iniciar_sesion'),
    path('tienda/cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),

    # URL Informes
    path('tienda/informes', views.informes, name='informes'),
    path('tienda/informe_marcas', views.informe_marcas, name='informe_marcas'),
    path('tienda/marcas_productos/<str:nombre>', views.marcas_productos, name='marcas_productos'),
    path('tienda/top_ten_productos', views.top_ten_productos, name='top_ten_productos'),
]
