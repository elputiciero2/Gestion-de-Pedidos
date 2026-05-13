from fastapi import Depends
from sqlalchemy.orm import Session

from .base_datos import obtener_sesion_bd
from .configuracion import Configuracion, obtener_configuracion


def obtener_configuracion_app() -> Configuracion:
    return obtener_configuracion()


def obtener_sesion_app(sesion: Session = Depends(obtener_sesion_bd)) -> Session:
    return sesion

