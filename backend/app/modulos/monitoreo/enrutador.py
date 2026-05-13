from fastapi import APIRouter
from .esquemas import FallaSolicitud, RecuperacionSolicitud

from .servicio import estado_monitoreo


enrutador = APIRouter(prefix="/monitoreo", tags=["monitoreo"])

@enrutador.get("/estado")
def leer_estado() -> dict[str, object]:
    return estado_monitoreo.obtener_estado()


@enrutador.post("/falla")
def simular_falla(solicitud: FallaSolicitud) -> dict[str, object]:
    estado_monitoreo.registrar_falla(solicitud.servicio, solicitud.detalle)
    return estado_monitoreo.obtener_estado()


@enrutador.post("/recuperar")
def recuperar(solicitud: RecuperacionSolicitud | None = None) -> dict[str, object]:
    estado_monitoreo.recuperar(solicitud.servicio if solicitud else None)
    return estado_monitoreo.obtener_estado()
