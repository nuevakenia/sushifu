from django.http import HttpResponse, request
from django.template import Template, Context
from django.template.loader import get_template

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from .forms import ExtendedUserCreationForm, UsuarioForm, ProductoForm
from mtv.models import Producto, Usuario, Carro
from django.contrib import messages
from django.db import connection
from django.core.files.base import ContentFile
import cx_Oracle

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

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
    productos = Producto.objects.all()
    data = {'productos':productos}
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

def activar_carro(request):
    
    if request.method == 'GET':
        usuario = request.user
        check_carro = Carro.objects.get(id_carro)    
        if check_carro == None:
            carro = Carro.objects.create(usuario.id,)
                
            #p_name = request.POST['p_name']
            # print(request.POST) 
            print(usuario.id)
            print(producto.nombre)
            print(carro.id)
    
    #print(producto)

    return render(request, 'productos/agregar_producto.html')


def desactivar_carro(request,id_carro):
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

def agregar_al_carro(request,id_producto):
    
    if request.method == 'GET':
        usuario = request.user
        producto = Producto.objects.get(id_producto=id_producto)
        print(usuario.id)
        print(producto.nombre)
        print(producto.id_producto)
        print(producto.descripcion)
        cantidad = 2
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

def modificar_carro(request,id_carro):
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

def eliminar_carro(request,id_carro):
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