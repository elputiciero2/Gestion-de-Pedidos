import os
from sqlalchemy.orm import sessionmaker, declarative_base
from app.servicios.gestor_conexion import GestorConexionMySQL


usuario_mysql = os.getenv("MYSQL_USER", "pedidos_usuario")
clave_mysql = os.getenv("MYSQL_PASSWORD", "pedidos_clave")
base_datos_mysql = os.getenv("MYSQL_DATABASE", "gestion_pedidos")

NODOS_MYSQL = {
    "nodo-1": os.getenv("DATABASE_URL_NODO1", f"mysql+pymysql://{usuario_mysql}:{clave_mysql}@mysql-nodo-1:3306/{base_datos_mysql}"),
    "nodo-2": os.getenv("DATABASE_URL_NODO2", f"mysql+pymysql://{usuario_mysql}:{clave_mysql}@mysql-nodo-2:3306/{base_datos_mysql}"),
    "nodo-3": os.getenv("DATABASE_URL_NODO3", f"mysql+pymysql://{usuario_mysql}:{clave_mysql}@mysql-nodo-3:3306/{base_datos_mysql}"),
}
gestor_conexion = GestorConexionMySQL(nodos=NODOS_MYSQL)
motor = gestor_conexion.obtener_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)
Base = declarative_base()

FabricaSesion = SessionLocal
motor_bd = motor

def obtener_sesion_bd():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def inicializar_base_datos():
    from app.modulos.auth.modelos import Usuario
    from app.modulos.pedidos.modelos import Pedido, DetallePedido
    from app.modelos.monitoreo import EventoFallover
    
    Base.metadata.create_all(bind=motor)
