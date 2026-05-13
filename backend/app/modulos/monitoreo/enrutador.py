from fastapi import APIRouter, Depends, HTTPException
from .esquemas import FallaSolicitud, RecuperacionSolicitud
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from .servicio import estado_monitoreo
from app.base_datos import gestor_conexion, SessionLocal
from app.modelos.monitoreo import EventoFallover
from app.modulos.auth.dependencias import obtener_usuario_actual


enrutador = APIRouter(prefix="/monitoreo", tags=["monitoreo"])


class ReporteFallo(BaseModel):
    nombre_nodo: str
    detalles: str = ""

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


@enrutador.get("/nodos/salud")
async def obtener_salud_nodos(usuario = Depends(obtener_usuario_actual)):
    """Retorna salud actual de todos los nodos MySQL"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "nodos": gestor_conexion.obtener_salud_todos()
    }


@enrutador.get("/eventos")
async def obtener_eventos_fallover(
    usuario = Depends(obtener_usuario_actual),
    limite: int = 50,
    offset: int = 0
):
    """Lista eventos de fallover (solo para admin)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    db = SessionLocal()
    try:
        eventos = db.query(EventoFallover)\
            .order_by(EventoFallover.timestamp.desc())\
            .limit(limite)\
            .offset(offset)\
            .all()
        
        return {
            "total": db.query(EventoFallover).count(),
            "eventos": [evento.a_dict() for evento in eventos]
        }
    finally:
        db.close()


@enrutador.post("/nodos/reportar-fallo")
async def reportar_fallo_nodo(
    reporte: ReporteFallo,
    usuario = Depends(obtener_usuario_actual)
):
    """Permite que frontend reporte fallo detectado"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    db = SessionLocal()
    try:
        evento = EventoFallover(
            tipo_evento="NODE_DOWN",
            nombre_nodo=reporte.nombre_nodo,
            detalles=reporte.detalles
        )
        db.add(evento)
        db.commit()
        
        gestor_conexion.reportar_fallo(reporte.nombre_nodo)
        
        return {"mensaje": "Fallo registrado", "evento": evento.a_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
