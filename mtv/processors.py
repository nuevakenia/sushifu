from mtv.models import Carro, Orden, Producto, Usuario

def carro_contador(request):
    usuario = request.user
    contador = Carro.objects.filter(id_carro=usuario.id).count()
    carro = Carro.objects.filter(id_carro=request.user.id)
    return {'carro_contador': contador}
