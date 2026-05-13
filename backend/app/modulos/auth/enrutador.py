from fastapi import APIRouter, Depends, status

from .dependencias import obtener_servicio_autenticacion, obtener_usuario_actual
from .esquemas import CredencialesLogin, RegistroUsuario, TokenRespuesta, UsuarioRespuesta
from .servicio import ServicioAutenticacion


enrutador_autenticacion = APIRouter(prefix="/autenticacion", tags=["autenticacion"])


@enrutador_autenticacion.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_usuario(
    solicitud: RegistroUsuario,
    servicio: ServicioAutenticacion = Depends(obtener_servicio_autenticacion),
) -> UsuarioRespuesta:
    return servicio.registrar_usuario(solicitud)


@enrutador_autenticacion.post("/login", response_model=TokenRespuesta)
def iniciar_sesion(
    solicitud: CredencialesLogin,
    servicio: ServicioAutenticacion = Depends(obtener_servicio_autenticacion),
) -> TokenRespuesta:
    usuario = servicio.autenticar_usuario(solicitud.correo, solicitud.clave)
    token = servicio.crear_token(usuario)
    return TokenRespuesta(token_acceso=token)


@enrutador_autenticacion.get("/me", response_model=UsuarioRespuesta)
def leer_usuario_actual(usuario=Depends(obtener_usuario_actual)) -> UsuarioRespuesta:
    return usuario
