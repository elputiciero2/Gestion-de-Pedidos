import pytest
from app.servicios.gestor_conexion import GestorConexionMySQL, EstadoNodo

def test_gestor_selecciona_nodo_sano():
    """Debe seleccionar un nodo sano cuando otros están caídos"""
    gestor = GestorConexionMySQL(
        nodos={
            "nodo-1": "mysql://user:pass@mysql-nodo-1:3306/gestion_pedidos",
            "nodo-2": "mysql://user:pass@mysql-nodo-2:3306/gestion_pedidos",
            "nodo-3": "mysql://user:pass@mysql-nodo-3:3306/gestion_pedidos",
        }
    )
    
    # Marcar nodo-1 como caído
    gestor.reportar_fallo("nodo-1")
    
    # Al pedir conexión, debe saltarse nodo-1
    nodo_seleccionado = gestor._seleccionar_nodo_activo()
    assert nodo_seleccionado in ["nodo-2", "nodo-3"]

def test_gestor_rotacion_round_robin():
    """Debe rotar entre nodos sanos de forma equitativa"""
    gestor = GestorConexionMySQL(
        nodos={
            "nodo-1": "mysql://user:pass@mysql-nodo-1:3306/gestion_pedidos",
            "nodo-2": "mysql://user:pass@mysql-nodo-2:3306/gestion_pedidos",
        }
    )
    
    nodo1 = gestor._seleccionar_nodo_activo()
    nodo2 = gestor._seleccionar_nodo_activo()
    assert nodo1 != nodo2

def test_gestor_recupera_nodo_caido():
    """Debe volver a habilitar nodo después de intentar conexión exitosa"""
    gestor = GestorConexionMySQL(
        nodos={
            "nodo-1": "mysql://user:pass@mysql-nodo-1:3306/gestion_pedidos",
        }
    )
    
    # Marcar como caído
    gestor.reportar_fallo("nodo-1")
    assert gestor.obtener_salud_nodo("nodo-1") == EstadoNodo.CAIDO
    
    # Reportar que el test de conexión tuvo éxito
    gestor.reportar_recuperacion("nodo-1")
    assert gestor.obtener_salud_nodo("nodo-1") == EstadoNodo.SANO
