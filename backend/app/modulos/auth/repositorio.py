from sqlalchemy import select
from sqlalchemy.orm import Session

from .modelos import Usuario


class RepositorioUsuario:
    def __init__(self, sesion: Session) -> None:
        self.sesion = sesion

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        consulta = select(Usuario).where(Usuario.correo == correo)
        return self.sesion.execute(consulta).scalars().first()

    def obtener_por_id(self, id_usuario: int) -> Usuario | None:
        return self.sesion.get(Usuario, id_usuario)

    def crear(self, usuario: Usuario) -> Usuario:
        self.sesion.add(usuario)
        self.sesion.commit()
        self.sesion.refresh(usuario)
        return usuario
