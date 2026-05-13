from fastapi import Depends
from sqlalchemy.orm import Session

from ...dependencias import obtener_sesion_app
from .repositorio import RepositorioPedidos
from .servicio import ServicioPedidos


def obtener_servicio_pedidos(
    sesion: Session = Depends(obtener_sesion_app),
) -> ServicioPedidos:
    return ServicioPedidos(RepositorioPedidos(sesion))
