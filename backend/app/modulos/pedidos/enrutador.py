from fastapi import APIRouter, Depends, HTTPException, status

from ..auth.dependencias import obtener_usuario_actual, requerir_admin
from ..auth.modelos import Usuario
from .dependencias import obtener_servicio_pedidos
from .esquemas import PedidoActualizar, PedidoCrear, PedidoEstadoActualizar, PedidoRespuesta
from .servicio import ServicioPedidos


enrutador = APIRouter(prefix="/pedidos", tags=["pedidos"])


@enrutador.post("", response_model=PedidoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    solicitud: PedidoCrear,
    usuario: Usuario = Depends(requerir_admin),
    servicio: ServicioPedidos = Depends(obtener_servicio_pedidos),
) -> PedidoRespuesta:
    return servicio.crear_pedido(usuario.id, solicitud)


@enrutador.get("", response_model=list[PedidoRespuesta])
def listar_pedidos(
    usuario: Usuario = Depends(obtener_usuario_actual),
    servicio: ServicioPedidos = Depends(obtener_servicio_pedidos),
) -> list[PedidoRespuesta]:
    usuario_id = None if usuario.rol == "admin" else usuario.id
    return servicio.listar_pedidos(usuario_id)


@enrutador.get("/{pedido_id}", response_model=PedidoRespuesta)
def obtener_pedido(
    pedido_id: int,
    usuario: Usuario = Depends(obtener_usuario_actual),
    servicio: ServicioPedidos = Depends(obtener_servicio_pedidos),
) -> PedidoRespuesta:
    pedido = servicio.obtener_pedido(pedido_id)
    if usuario.rol != "admin" and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    return pedido


@enrutador.put("/{pedido_id}", response_model=PedidoRespuesta)
def actualizar_pedido(
    pedido_id: int,
    solicitud: PedidoActualizar,
    usuario: Usuario = Depends(requerir_admin),
    servicio: ServicioPedidos = Depends(obtener_servicio_pedidos),
) -> PedidoRespuesta:
    pedido = servicio.obtener_pedido(pedido_id)
    if usuario.rol != "admin" and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    return servicio.actualizar_pedido(pedido, solicitud)


@enrutador.patch("/{pedido_id}/estado", response_model=PedidoRespuesta)
def actualizar_estado_pedido(
    pedido_id: int,
    solicitud: PedidoEstadoActualizar,
    usuario: Usuario = Depends(requerir_admin),
    servicio: ServicioPedidos = Depends(obtener_servicio_pedidos),
) -> PedidoRespuesta:
    pedido = servicio.obtener_pedido(pedido_id)
    if usuario.rol != "admin" and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    return servicio.actualizar_estado(pedido, solicitud.estado)


@enrutador.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(
    pedido_id: int,
    usuario: Usuario = Depends(requerir_admin),
    servicio: ServicioPedidos = Depends(obtener_servicio_pedidos),
) -> None:
    pedido = servicio.obtener_pedido(pedido_id)
    if usuario.rol != "admin" and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    servicio.eliminar_pedido(pedido)
