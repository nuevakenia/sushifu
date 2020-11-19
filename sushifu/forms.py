from django import forms
from django.forms import ModelForm
from mtv.models import Usuario, Producto, Carro
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre','apellido','direccion','comuna','provincia', 'region', 'fecha_nacimiento','sexo','telefono')

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('id_producto','nombre','tipo','descripcion','stock','precio','catalogo','imagen')


class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ('id_carro','nombre_producto','precio_producto','cantidad_producto')