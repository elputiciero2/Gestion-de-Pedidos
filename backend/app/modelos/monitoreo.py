from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
from typing import Dict, Any

Base = declarative_base()

class EventoFallover(Base):
    __tablename__ = "eventos_fallover"
    
    id = Column(Integer, primary_key=True)
    tipo_evento = Column(String(20), nullable=False)
    nombre_nodo = Column(String(50), nullable=False)
    detalles = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, tipo_evento: str, nombre_nodo: str, detalles: str = None):
        self.tipo_evento = tipo_evento
        self.nombre_nodo = nombre_nodo
        self.detalles = detalles
        self.timestamp = datetime.utcnow()
    
    def a_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tipo_evento": self.tipo_evento,
            "nombre_nodo": self.nombre_nodo,
            "detalles": self.detalles,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
