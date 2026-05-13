import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("CREAR_TABLAS", "false")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite://")

from app import modelos as modelos_app
from app.base_datos import Base
from app.dependencias import obtener_sesion_app
from app.main import aplicacion
from app.configuracion import obtener_configuracion
from app.modulos.auth.repositorio import RepositorioUsuario
from app.modulos.auth.servicio import ServicioAutenticacion
from app.modulos.monitoreo.servicio import estado_monitoreo


@pytest.fixture
def cliente():
    motor = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=motor)
    fabrica_sesion = sessionmaker(bind=motor, autoflush=False, autocommit=False, future=True)
    configuracion = obtener_configuracion()

    sesion_inicial = fabrica_sesion()
    try:
        repositorio = RepositorioUsuario(sesion_inicial)
        servicio = ServicioAutenticacion(repositorio, configuracion)
        servicio.asegurar_admin_predeterminado(
            configuracion.admin_nombre,
            configuracion.admin_correo,
            configuracion.admin_clave,
        )
    finally:
        sesion_inicial.close()

    def obtener_sesion_pruebas():
        sesion = fabrica_sesion()
        try:
            yield sesion
        finally:
            sesion.close()

    aplicacion.dependency_overrides[obtener_sesion_app] = obtener_sesion_pruebas
    estado_monitoreo.recuperar()
    with TestClient(aplicacion) as cliente_pruebas:
        yield cliente_pruebas
    aplicacion.dependency_overrides.clear()
