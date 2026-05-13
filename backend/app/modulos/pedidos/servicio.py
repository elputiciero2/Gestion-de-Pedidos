from fastapi import HTTPException, status

from .esquemas import PedidoActualizar, PedidoCrear
from .modelos import DetallePedido, Pedido
from .repositorio import RepositorioPedidos

TRANSICIONES_PEDIDO: dict[str, set[str]] = {
    "pendiente": {"en_proceso"},
    "en_proceso": {"enviado"},
    "enviado": {"entregado"},
    "entregado": set(),
}


class ServicioPedidos:
    def __init__(self, repositorio: RepositorioPedidos) -> None:
        self.repositorio = repositorio

    def crear_pedido(self, usuario_id: int, datos: PedidoCrear) -> Pedido:
        detalles = []
        total = 0.0
        for detalle in datos.detalles:
            subtotal = float(detalle.cantidad) * float(detalle.precio_unitario)
            total += subtotal
            detalles.append(
                DetallePedido(
                    nombre_producto=detalle.nombre_producto,
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                    subtotal=subtotal,
                )
            )
        pedido = Pedido(
            usuario_id=usuario_id,
            estado="pendiente",
            direccion_entrega=datos.direccion_entrega,
            total=total,
            detalles=detalles,
        )
        return self.repositorio.crear(pedido)

    def listar_pedidos(self, usuario_id: int | None = None) -> list[Pedido]:
        return self.repositorio.listar(usuario_id)

    def obtener_pedido(self, pedido_id: int) -> Pedido:
        pedido = self.repositorio.obtener(pedido_id)
        if not pedido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
        return pedido

    def actualizar_pedido(self, pedido: Pedido, datos: PedidoActualizar) -> Pedido:
        if datos.direccion_entrega is not None:
            pedido.direccion_entrega = datos.direccion_entrega
        if datos.detalles is not None:
            pedido.detalles.clear()
            total = 0.0
            for detalle in datos.detalles:
                subtotal = float(detalle.cantidad) * float(detalle.precio_unitario)
                total += subtotal
                pedido.detalles.append(
                    DetallePedido(
                        nombre_producto=detalle.nombre_producto,
                        cantidad=detalle.cantidad,
                        precio_unitario=detalle.precio_unitario,
                        subtotal=subtotal,
                    )
                )
            pedido.total = total
        return self.repositorio.guardar(pedido)

    def eliminar_pedido(self, pedido: Pedido) -> None:
        self.repositorio.eliminar(pedido)

    def actualizar_estado(self, pedido: Pedido, nuevo_estado: str) -> Pedido:
        estado_actual = pedido.estado
        if nuevo_estado == estado_actual:
            return pedido
        permitidos = TRANSICIONES_PEDIDO.get(estado_actual, set())
        if nuevo_estado not in permitidos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transicion de estado no permitida",
            )
        pedido.estado = nuevo_estado
        return self.repositorio.guardar(pedido)
