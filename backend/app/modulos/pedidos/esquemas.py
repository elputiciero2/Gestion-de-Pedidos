from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EstadoPedido = Literal["pendiente", "en_proceso", "enviado", "entregado"]


class DetallePedidoCrear(BaseModel):
    nombre_producto: str = Field(min_length=1)
    cantidad: int = Field(gt=0)
    precio_unitario: float = Field(gt=0)


class PedidoCrear(BaseModel):
    direccion_entrega: str = Field(min_length=1)
    detalles: list[DetallePedidoCrear]


class PedidoActualizar(BaseModel):
    direccion_entrega: str | None = None
    detalles: list[DetallePedidoCrear] | None = None


class PedidoEstadoActualizar(BaseModel):
    estado: EstadoPedido


class DetallePedidoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class PedidoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    estado: EstadoPedido
    direccion_entrega: str
    total: float
    creado_en: datetime
    actualizado_en: datetime
    detalles: list[DetallePedidoRespuesta]
