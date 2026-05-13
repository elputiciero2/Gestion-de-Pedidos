from pydantic import BaseModel


class SaludDetalle(BaseModel):
    estado: str
    detalle: str
    actualizado_en: str
