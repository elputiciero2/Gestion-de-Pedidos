from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy import create_engine, text, event
from sqlalchemy.pool import QueuePool
import logging

logger = logging.getLogger(__name__)

class EstadoNodo(Enum):
    SANO = "sano"
    CAIDO = "caído"
    TESTING = "testing"

class GestorConexionMySQL:
    def __init__(self, nodos: Dict[str, str], intervalo_reintento: int = 30):
        """
        Args:
            nodos: dict con {nombre: connection_string}
            intervalo_reintento: segundos antes de reintentar nodo caído
        """
        self.nodos = nodos
        self.intervalo_reintento = intervalo_reintento
        self.estado_nodos = {nombre: EstadoNodo.SANO for nombre in nodos}
        self.timestamp_fallo = {}
        self.indice_rotacion = 0
        self.engine = None
        self._crear_engine()
    
    def _crear_engine(self):
        """Crea engine con pool de conexiones"""
        url_primaria = list(self.nodos.values())[0]
        self.engine = create_engine(
            url_primaria,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=False
        )
        
        @event.listens_for(self.engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            dbapi_conn.ping(False)
    
    def _seleccionar_nodo_activo(self) -> str:
        """Retorna nombre del siguiente nodo sano usando round-robin"""
        nodos_sanos = [
            n for n in self.nodos.keys() 
            if self._puede_intentar_nodo(n)
        ]
        
        if not nodos_sanos:
            return list(self.nodos.keys())[0]
        
        self.indice_rotacion = (self.indice_rotacion + 1) % len(nodos_sanos)
        return nodos_sanos[self.indice_rotacion]
    
    def _puede_intentar_nodo(self, nombre: str) -> bool:
        """Verifica si es momento de reintentar nodo caído"""
        if self.estado_nodos[nombre] == EstadoNodo.SANO:
            return True
        
        if nombre not in self.timestamp_fallo:
            return True
        
        tiempo_transcurrido = datetime.now() - self.timestamp_fallo[nombre]
        return tiempo_transcurrido >= timedelta(seconds=self.intervalo_reintento)
    
    def reportar_fallo(self, nombre_nodo: str):
        """Marca nodo como caído"""
        self.estado_nodos[nombre_nodo] = EstadoNodo.CAIDO
        self.timestamp_fallo[nombre_nodo] = datetime.now()
        logger.warning(f"Nodo {nombre_nodo} marcado como caído")
    
    def reportar_recuperacion(self, nombre_nodo: str):
        """Marca nodo como recuperado"""
        self.estado_nodos[nombre_nodo] = EstadoNodo.SANO
        self.timestamp_fallo.pop(nombre_nodo, None)
        logger.info(f"Nodo {nombre_nodo} recuperado")
    
    def obtener_salud_nodo(self, nombre_nodo: str) -> EstadoNodo:
        """Retorna estado actual del nodo"""
        return self.estado_nodos[nombre_nodo]
    
    def obtener_salud_todos(self) -> Dict[str, str]:
        """Retorna estado de todos los nodos"""
        return {
            nombre: self.estado_nodos[nombre].value 
            for nombre in self.nodos.keys()
        }
    
    def obtener_engine(self):
        """Retorna engine SQLAlchemy para usar en la aplicación"""
        return self.engine
