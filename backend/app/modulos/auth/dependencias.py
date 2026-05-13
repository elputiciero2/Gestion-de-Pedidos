from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ...dependencias import obtener_configuracion_app, obtener_sesion_app
from .modelos import Usuario
from .repositorio import RepositorioUsuario
from .servicio import ServicioAutenticacion

esquema_oauth = OAuth2PasswordBearer(tokenUrl="/api/autenticacion/login")


def obtener_servicio_autenticacion(
    sesion: Session = Depends(obtener_sesion_app),
) -> ServicioAutenticacion:
    return ServicioAutenticacion(RepositorioUsuario(sesion), obtener_configuracion_app())


def obtener_usuario_actual(
    token: str = Depends(esquema_oauth),
    servicio: ServicioAutenticacion = Depends(obtener_servicio_autenticacion),
) -> Usuario:
    return servicio.obtener_usuario_desde_token(token)


def requerir_admin(usuario: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
    if usuario.rol != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    return usuario
