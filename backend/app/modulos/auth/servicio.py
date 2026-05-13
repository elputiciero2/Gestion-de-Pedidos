from datetime import datetime, timedelta, timezone

from jose import jwt
from fastapi import HTTPException, status
from jose.exceptions import JWTError
from passlib.hash import pbkdf2_sha256

from ...configuracion import Configuracion
from .esquemas import RegistroUsuario
from .modelos import Usuario
from .repositorio import RepositorioUsuario
class ServicioAutenticacion:
    def __init__(self, repositorio: RepositorioUsuario, configuracion: Configuracion) -> None:
        self.repositorio = repositorio
        self.configuracion = configuracion

    def crear_hash(self, clave: str) -> str:
        return pbkdf2_sha256.hash(clave)

    def verificar_clave(self, clave: str, clave_hash: str) -> bool:
        return pbkdf2_sha256.verify(clave, clave_hash)

    def registrar_usuario(self, solicitud: RegistroUsuario) -> Usuario:
        existente = self.repositorio.obtener_por_correo(solicitud.correo)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ya existe")
        usuario = Usuario(
            nombre=solicitud.nombre,
            correo=solicitud.correo,
            clave_hash=self.crear_hash(solicitud.clave),
            rol=solicitud.rol,
        )
        return self.repositorio.crear(usuario)

    def autenticar_usuario(self, correo: str, clave: str) -> Usuario:
        usuario = self.repositorio.obtener_por_correo(correo)
        if not usuario or not self.verificar_clave(clave, usuario.clave_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
        return usuario

    def crear_token(self, usuario: Usuario) -> str:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=self.configuracion.minutos_token)
        datos = {"id_usuario": str(usuario.id), "rol": usuario.rol, "exp": expiracion}
        return jwt.encode(datos, self.configuracion.llave_secreta, algorithm=self.configuracion.algoritmo_jwt)

    def obtener_usuario_desde_token(self, token: str) -> Usuario:
        try:
            datos = jwt.decode(
                token,
                self.configuracion.llave_secreta,
                algorithms=[self.configuracion.algoritmo_jwt],
            )
        except JWTError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido",
            ) from error
        id_usuario = datos.get("id_usuario")
        if not id_usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
        usuario = self.repositorio.obtener_por_id(int(id_usuario))
        if not usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
        return usuario

    def asegurar_admin_predeterminado(
        self,
        nombre: str,
        correo: str,
        clave: str,
    ) -> Usuario:
        usuario = self.repositorio.obtener_por_correo(correo)
        if usuario:
            return usuario
        return self.repositorio.crear(
            Usuario(
                nombre=nombre,
                correo=correo,
                clave_hash=self.crear_hash(clave),
                rol="admin",
            )
        )
