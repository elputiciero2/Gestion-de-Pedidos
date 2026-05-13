from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .base_datos import Base, FabricaSesion, motor_bd
from .configuracion import obtener_configuracion
from .modulos.auth.enrutador import enrutador_autenticacion
from .modulos.auth.repositorio import RepositorioUsuario
from .modulos.auth.servicio import ServicioAutenticacion
from .modulos.monitoreo.enrutador import enrutador as enrutador_monitoreo
from .modulos.pedidos.enrutador import enrutador as enrutador_pedidos
from .modulos.salud.rutas import enrutador as enrutador_salud


configuracion = obtener_configuracion()
aplicacion = FastAPI(title=configuracion.nombre_app, version="0.1.0")

aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=list(configuracion.origenes_cors),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

aplicacion.include_router(enrutador_autenticacion, prefix=configuracion.ruta_api)
aplicacion.include_router(enrutador_pedidos, prefix=configuracion.ruta_api)
aplicacion.include_router(enrutador_salud, prefix=configuracion.ruta_api)
aplicacion.include_router(enrutador_monitoreo, prefix=configuracion.ruta_api)


@aplicacion.on_event("startup")
def iniciar_base_datos() -> None:
    if configuracion.crear_tablas:
        from . import modelos as modelos_app

        Base.metadata.create_all(bind=motor_bd)
        sesion = FabricaSesion()
        try:
            repositorio = RepositorioUsuario(sesion)
            servicio = ServicioAutenticacion(repositorio, configuracion)
            servicio.asegurar_admin_predeterminado(
                configuracion.admin_nombre,
                configuracion.admin_correo,
                configuracion.admin_clave,
            )
        finally:
            sesion.close()
