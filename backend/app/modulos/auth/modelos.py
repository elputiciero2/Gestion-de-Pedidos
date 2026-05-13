from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ...base_datos import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)
    correo = Column(String(120), unique=True, index=True, nullable=False)
    clave_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False, default="usuario")
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    pedidos = relationship("Pedido", back_populates="usuario", cascade="all, delete-orphan")
