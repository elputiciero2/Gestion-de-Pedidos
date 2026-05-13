from dataclasses import dataclass
from functools import lru_cache
from os import getenv


@dataclass(slots=True)
class Configuracion:
    nombre_app: str = getenv("NOMBRE_APP", "gestion-pedidos")
    entorno: str = getenv("ENTORNO", "desarrollo")
    ruta_api: str = getenv("RUTA_API", "/api")
    llave_secreta: str = getenv("LLAVE_SECRETA", "cambia-esta-llave")
    algoritmo_jwt: str = getenv("ALGORITMO_JWT", "HS256")
    minutos_token: int = int(getenv("MINUTOS_TOKEN", "60"))
    crear_tablas: bool = getenv("CREAR_TABLAS", "true").lower() in ("1", "true", "si", "yes")
    admin_nombre: str = getenv("ADMIN_NOMBRE", "Administrador")
    admin_correo: str = getenv("ADMIN_CORREO", "admin@gestion-pedidos.local")
    admin_clave: str = getenv("ADMIN_CLAVE", "Admin123!")
    cadenas_conexion_bd: tuple[str, ...] = tuple(
        cadena.strip()
        for cadena in getenv(
            "DATABASE_URLS",
            getenv(
                "DATABASE_URL",
                "mysql+pymysql://pedidos_usuario:pedidos_clave@mysql:3306/pedidos?charset=utf8mb4",
            ),
        ).split(",")
        if cadena.strip()
    )
    origenes_cors: tuple[str, ...] = tuple(
        origen.strip()
        for origen in getenv("ORIGENES_CORS", "http://localhost:8080").split(",")
        if origen.strip()
    )

    @property
    def cadena_conexion(self) -> str:
        return self.cadenas_conexion_bd[0]


@lru_cache(maxsize=1)
def obtener_configuracion() -> Configuracion:
    return Configuracion()
