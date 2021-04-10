"""sushifu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from sushifu.views import (navbar,about, agregar_al_carro, agregar_producto, catalogo, 
contacto, eliminar_carro, eliminar_producto, enviar_pedido, 
anular_pedido, inicio, listado_carro, listado_producto, 
modificar_producto, pagina_login, pagina_logout, pagina_registro, plantilla)
from sushifu import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', inicio, name='inicio'),
    path('inicio/', views.inicio, name="inicio"),
    path('admin/', admin.site.urls),
    path('about/', about, name="about"),
    path('contacto/', contacto, name="contacto"),
    path('productos/listado_producto/', listado_producto, name="listado_producto"),
    path('productos/agregar_producto/', agregar_producto, name="agregar_producto"),
    path('productos/modificar_producto/<id_producto>/', modificar_producto, name="modificar_producto"),
    path('productos/eliminar_producto/<id_producto>/', eliminar_producto, name="eliminar_producto"),
    path('productos/catalogo/', catalogo, name="catalogo"),
    path('registro/', pagina_registro, name="registro"),
    path('login/', pagina_login, name="login"),
    path('logout/', pagina_logout, name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
    path('agregar_carro/<id_producto>/', agregar_al_carro, name="agregar_al_carro"),
    path('listado_carro/', listado_carro, name="listado_carro"),
    path('eliminar_carro/<id>/', eliminar_carro, name="eliminar_carro"),
    path('enviar_pedido/', enviar_pedido, name="enviar_pedido"),
    path('anular_pedido/<id_orden>/', anular_pedido, name="anular_pedido"),
    path('navbar/', navbar, name="navbar"),
    path('plantilla/', plantilla, name="plantilla"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
