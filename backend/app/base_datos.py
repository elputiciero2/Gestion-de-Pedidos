from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .configuracion import obtener_configuracion


configuracion = obtener_configuracion()
motor_bd = create_engine(configuracion.cadena_conexion, pool_pre_ping=True, future=True)
FabricaSesion = sessionmaker(bind=motor_bd, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def obtener_sesion_bd() -> Generator[Session, None, None]:
    sesion = FabricaSesion()
    try:
        yield sesion
    finally:
        sesion.close()
