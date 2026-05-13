from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RolUsuario = Literal["admin", "usuario"]


class RegistroUsuario(BaseModel):
    nombre: str = Field(min_length=1)
    correo: str = Field(min_length=3)
    clave: str = Field(min_length=6)
    rol: RolUsuario = "usuario"


class CredencialesLogin(BaseModel):
    correo: str = Field(min_length=3)
    clave: str = Field(min_length=6)


class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: str
    rol: RolUsuario


class TokenRespuesta(BaseModel):
    token_acceso: str
    tipo: str = "bearer"
