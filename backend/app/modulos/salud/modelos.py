from dataclasses import dataclass


@dataclass(slots=True)
class EstadoSalud:
    estado: str
    detalle: str
    actualizado_en: str
