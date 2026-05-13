from pydantic import BaseModel


class FallaSolicitud(BaseModel):
    servicio: str = "backend-nodo-1"
    detalle: str | None = None


class RecuperacionSolicitud(BaseModel):
    servicio: str | None = None
