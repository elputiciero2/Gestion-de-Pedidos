from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .modelos import Pedido


class RepositorioPedidos:
    def __init__(self, sesion: Session) -> None:
        self.sesion = sesion

    def crear(self, pedido: Pedido) -> Pedido:
        self.sesion.add(pedido)
        self.sesion.commit()
        self.sesion.refresh(pedido)
        return pedido

    def guardar(self, pedido: Pedido) -> Pedido:
        self.sesion.add(pedido)
        self.sesion.commit()
        self.sesion.refresh(pedido)
        return pedido

    def obtener(self, pedido_id: int) -> Pedido | None:
        consulta = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .options(selectinload(Pedido.detalles))
        )
        return self.sesion.execute(consulta).scalars().first()

    def listar(self, usuario_id: int | None = None) -> list[Pedido]:
        consulta = select(Pedido).options(selectinload(Pedido.detalles))
        if usuario_id is not None:
            consulta = consulta.where(Pedido.usuario_id == usuario_id)
        return list(self.sesion.execute(consulta).scalars().all())

    def eliminar(self, pedido: Pedido) -> None:
        self.sesion.delete(pedido)
        self.sesion.commit()
