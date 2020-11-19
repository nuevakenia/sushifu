from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=99)
    comuna = models.CharField(max_length=99)
    provincia = models.CharField(max_length=99)
    region = models.CharField(max_length=99)
    fecha_nacimiento = models.DateTimeField(default=timezone.now, null=True)
    sexo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=99)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=99)
    stock = models.IntegerField()
    precio = models.IntegerField()
    catalogo = models.BooleanField()
    imagen = models.ImageField(null=True, blank=True, upload_to="uploads/")
    
    def __str__(self):
        return self.nombre

class Carro(models.Model):
    id_carro = models.IntegerField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=50)
    precio_producto = models.IntegerField(default='0')
    cantidad_producto = models.IntegerField(default='0')
   # def __int__(self):
     #   return self.id_carro


class Orden(models.Model):
    id_orden = models.IntegerField(primary_key=True)
    id_carro = models.OneToOneField('Carro', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)
    nombre_cliente = models.CharField(max_length=50)
    direccion = models.CharField(max_length=99)
    nota = models.CharField(max_length=200)
    total= models.IntegerField(default='0')
  #  def __str__(self):
  #      return self.id_orden

class Boleta(models.Model):
    id_boleta = models.IntegerField(primary_key=True)
    id_orden = models.OneToOneField('Orden', on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.IntegerField(default='0')
   # def __str__(self):
   #     return self.id_boleta

class Reporte(models.Model):
    id_reporte = models.IntegerField(primary_key=True)
    id_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    fecha_periodo = models.DateTimeField(default=timezone.now)
    total_boleta = models.IntegerField()
    total_periodo = models.IntegerField()
  #  def __str__(self):
  #      return self.id_reporte
