import pytest
from datetime import datetime
from app.modelos.monitoreo import EventoFallover

def test_evento_fallover_creacion():
    """Debe crear evento con timestamp automático"""
    evento = EventoFallover(
        tipo_evento="NODE_DOWN",
        nombre_nodo="nodo-2",
        detalles="Connection refused on port 3306"
    )
    
    assert evento.tipo_evento == "NODE_DOWN"
    assert evento.nombre_nodo == "nodo-2"
    assert isinstance(evento.timestamp, datetime)
    assert evento.detalles == "Connection refused on port 3306"

def test_evento_fallover_node_up():
    """Debe soportar evento NODE_UP"""
    evento = EventoFallover(
        tipo_evento="NODE_UP",
        nombre_nodo="nodo-1",
        detalles="Recovered after 45 seconds"
    )
    
    assert evento.tipo_evento == "NODE_UP"

def test_evento_fallover_serializacion():
    """Debe convertirse a dict para JSON"""
    evento = EventoFallover(
        tipo_evento="NODE_DOWN",
        nombre_nodo="nodo-3",
        detalles="Timeout"
    )
    
    evento_dict = evento.a_dict()
    assert "timestamp" in evento_dict
    assert evento_dict["tipo_evento"] == "NODE_DOWN"
