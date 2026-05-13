from fastapi import APIRouter, Response, status

from .servicio import servicio_salud
from .esquemas import SaludDetalle


enrutador = APIRouter(prefix="/salud", tags=["salud"])


@enrutador.get("")
def verificar_salud(respuesta: Response) -> dict[str, str]:
    estado = servicio_salud.verificar()
    if estado["estado"] != "ok":
        respuesta.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return estado


@enrutador.get("/detalle", response_model=SaludDetalle)
def verificar_salud_detalle() -> dict[str, str]:
    return servicio_salud.verificar_detalle()
