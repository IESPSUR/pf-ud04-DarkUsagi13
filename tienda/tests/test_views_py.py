from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tienda.models import Producto, Marca


# Create your tests here.

class TestViewLogin(TestCase):
    def setUp(self):
        self.register_url = reverse('registrar_usuario')
        self.login_url = reverse('iniciar_sesion')
        self.user = {
            'username': 'user_test',
            'password': 'Django-123',
        }
        self.marca = Marca.objects.create(nombre="Adidas")
        self.producto = Producto.objects.create(
            marca=self.marca, nombre="Force", modelo="1", unidades="50", precio="100", detalles=""
        )
        self.checkout_url = reverse('checkout', kwargs={"pk": self.producto.pk})
        return super().setUp()

    def test_register(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response = self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'tienda/iniciar_sesion.html')

    def test_login_success(self):
        self.client.post(self.login_url,self.user,format='text/html')
        user = User.objects.create_user(**self.user)
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_checkout_success(self):
        response = self.client.get(self.checkout_url)
        listado = reverse('listado_compra')
        self.assertContains(response, 'href="{0}"'.format(listado))
        self.assertTemplateUsed(response,'tienda/compra.html')

