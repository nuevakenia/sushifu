function confirmarEliminacion(id_producto) {
    Swal.fire({
        title: '¿Estás seguro/a?',
        text: "No podrás revertir esta acción!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, Borrar!'
      }).then((result) => {
        if (result.isConfirmed) {
          //redirigir al usuario
          window.location.href ="/productos/eliminar_producto/"+id_producto+"/";
        }
      })
}

function confirmarAgregar(id_producto) {
  Swal.fire({
      title: '¿Estás seguro/a?',
      text: "Agregaras este producto al carro de compras!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si, Agregar!'
    }).then((result) => {
      if (result.isConfirmed) {
        //redirigir al usuario
        window.location.href ="/agregar_carro/"+id_producto+"/";
      }
    })
}