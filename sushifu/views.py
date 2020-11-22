from django.http import HttpResponse, request
from django.template import Template, Context
from django.template.loader import get_template
from django.utils import timezone
from django.db.models.functions import Concat

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from .forms import ExtendedUserCreationForm, UsuarioForm, ProductoForm
from mtv.models import Carro, Orden, Producto, Usuario
from django.contrib import messages
from django.db import connection
from django.core.files.base import ContentFile
import cx_Oracle
import locale

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.aggregates import Sum

def about(request):

    return render(request, "about.html")

def contacto(request):

    return render(request, "contacto.html")

def navbar(request):

    return render(request, "navbar.html")    

@login_required(login_url="login")
@staff_member_required
def listado_producto(request):
    productos = Producto.objects.all()
    data = {'productos':productos}
    return render(request, "productos/listado_producto.html", data)

@login_required(login_url="login")
@staff_member_required
def agregar_producto(request):
    data = {
        'form':ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Guardado correctamente"
        data['form'] = formulario

    return render(request, 'productos/agregar_producto.html',data)

@login_required(login_url="login")
@staff_member_required
def modificar_producto(request, id_producto):
    producto = Producto.objects.get(id_producto=id_producto)
    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Guardado correctamente"
        data['form'] = ProductoForm(instance=Producto.objects.get(id_producto=id_producto))

    return render(request, 'productos/modificar_producto.html',data)

@login_required(login_url="login")
@staff_member_required
def eliminar_producto(request, id_producto):
    producto = Producto.objects.get(id_producto=id_producto)
    producto.delete()

    return redirect(to=listado_producto)

def catalogo(request):
    usuario = request.user
    productos = Producto.objects.all()
    contador = Carro.objects.filter(id_carro=usuario.id).count()
    data = {'productos':productos, 'contador':contador}
    return render(request, "productos/catalogo.html", data)

def inicio(request):
    
    return render(request, "inicio.html")


def pagina_logout(request):
    logout(request)
    return redirect('login')


def pagina_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.warning(request, 'Identificación Correcta!')
            return redirect('inicio')

        else:
            messages.warning(request, 'Identificación Incorrecta!')

    return render(request, 'login.html',{'titulo':'Indentifícate'})

def pagina_registro(request):
        if request.method == 'POST':
            formularioRegistro = UserCreationForm(request.POST)
            usuario_form = UsuarioForm(request.POST)
            password = request.POST["password1"]
            confirmation = request.POST["password2"]
            if password != confirmation:
                messages.warning(request, 'Identificación Correcta!')
            if formularioRegistro.is_valid and usuario_form.is_valid():
                user = formularioRegistro.save()

                usuario = usuario_form.save(commit=False)
                usuario.user = user

                usuario.save()

                username = formularioRegistro.cleaned_data.get('username')
                password = formularioRegistro.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                
                return redirect('inicio')
        else:
            formularioRegistro = ExtendedUserCreationForm()
            usuario_form = UsuarioForm()

        context = {'formularioRegistro' : formularioRegistro, 'usuario_form' : usuario_form}
        return render(request, 'registro.html', context)

# CARRO

def limpiar_carro(request,id_carro):
    data = {
        'form':ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Guardado correctamente"
        data['form'] = formulario

    return render(request, 'limpiar_carro.html',data)

@login_required(login_url="login")
def agregar_al_carro(request,id_producto):
    
    if request.method == 'GET':
        usuario = request.user
        producto = Producto.objects.get(id_producto=id_producto)
        print(usuario.id)
        print(producto.nombre)
        print(producto.id_producto)
        print(producto.descripcion)
        cantidad = 1
        #if Carro.objects.filter(id_carro=usuario.id).exists():
            #print("ya existe")
           # print(Carro.objects.filter(id_carro=usuario.id))
        #else:
        carro = Carro.objects.create(id_carro=usuario.id,id_producto=producto,nombre_producto=producto.nombre,precio_producto=producto.precio, cantidad_producto=cantidad)
        print(carro)
       # carro = Carro.objects.set(usuario.id,producto.id_producto,producto.nombre,producto.precio,cantidad)
        #p_name = request.POST['p_name']
        # print(request.POST) 
        
       # print(carro.nombre_producto)
    
    
    return render(request, 'agregar_carro.html')

@login_required(login_url="login")
def enviar_pedido(request):
    if request.method == 'GET':
        locale.setlocale(locale.LC_ALL, '')
        usuario = request.user
        usuario2 = Usuario.objects.get(id=usuario.id)
        carros = Carro.objects.filter(id_carro=usuario.id)
        carro = Carro.objects.filter(id_carro=usuario.id).first()
        total = locale.format('%.0f',Carro.objects.filter(id_carro=usuario.id).aggregate(sum=Sum('precio_producto'))['sum'], grouping=True, monetary=True)
        total2 = Carro.objects.filter(id_carro=usuario.id).aggregate(sum=Sum('precio_producto'))['sum']
        orden = Orden.objects.create(id_carro=carro,fecha_hora=timezone.now(),nombre_cliente=usuario2.nombre+' '+usuario2.apellido,direccion=usuario2.direccion,nota='',total=total2)
        data = {'orden':orden,'total':total}
    return render(request, 'enviar_pedido.html', data)

@login_required(login_url="login")
def eliminar_carro(request,id):
    carro = Carro.objects.get(id=id)
    carro.delete()
    return redirect(to=listado_carro)

@login_required(login_url="login")
def listado_carro(request):
    usuario = request.user
    usuario2 = Usuario.objects.get(id=usuario.id)
    locale.setlocale(locale.LC_ALL, '')
   # carro = Carro.objects.get(id_carro=usuario.id)
    #id_producto = carro.id_producto
  #  producto = Producto.objects.get(id_producto=id_producto)
   # id_carro = usuario.id
    carros = Carro.objects.filter(id_carro=usuario.id)
    carro = Carro.objects.filter(id_carro=usuario.id).first()
    orden2 = Orden.objects.all().last()   
    #productos = Producto.objects.all(id_producto=carros.id_carro)
    total = locale.format('%.0f',Carro.objects.filter(id_carro=usuario.id).aggregate(sum=Sum('precio_producto'))['sum'], grouping=True, monetary=True)
    total2 = Carro.objects.filter(id_carro=usuario.id).aggregate(sum=Sum('precio_producto'))['sum']
    data = {'carros':carros,'total':total,'carro':carro}
    return render(request, "listado_carro.html", data)

 #sumar precio_producto

def anular_pedido(request, id_orden):
    if request.method == 'GET':
        usuario = request.user
        usuario2 = Usuario.objects.get(id=usuario.id)
        carros = Carro.objects.filter(id_carro=usuario.id)
        carro = Carro.objects.filter(id_carro=usuario.id).first()
        ordenes = Orden.objects.get(id_orden=id_orden)
        print(ordenes.id_orden)
        if Orden.objects.get(id_orden=id_orden).exist():
            orden2 = ordenes
            ordenes.delete()
            data = {'orden2':orden2}   
        else:
            print('No existe')
            redirect(to=listado_carro)
    return render(request, 'anular_pedido.html', data)