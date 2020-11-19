from django.test import TestCase
from django.db import connection
# Create your tests here.
import unittest
from django.urls import reverse, resolve
from trisix.views import listado_producto, agregar_producto, about

class TestUrls(unittest.TestCase):

    def test_login_url(self):
        url = reverse('listado_producto')
        self.assertEquals(resolve(url).func, listado_producto)
    
    def test_about_url(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func, about)
        