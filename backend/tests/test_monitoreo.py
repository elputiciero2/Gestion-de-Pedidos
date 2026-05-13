def test_falla_y_recuperacion(cliente):
    respuesta_estado = cliente.get("/api/monitoreo/estado")
    assert respuesta_estado.status_code == 200
    assert respuesta_estado.json()["estado"] == "ok"
    assert "servicios" in respuesta_estado.json()
    assert len(respuesta_estado.json()["servicios"]) >= 3

    respuesta_falla = cliente.post(
        "/api/monitoreo/falla",
        json={"servicio": "backend-nodo-1", "detalle": "nodo caido"},
    )
    assert respuesta_falla.status_code == 200
    assert respuesta_falla.json()["estado"] == "falla"
    assert respuesta_falla.json()["servicio_afectado"] == "backend-nodo-1"
    assert respuesta_falla.json()["incidencia_actual"]["detalle"] == "nodo caido"
    assert respuesta_falla.json()["resumen"]["caidos"] == 1

    respuesta_salud = cliente.get("/api/salud")
    assert respuesta_salud.status_code == 503
    assert respuesta_salud.json()["estado"] == "falla"

    respuesta_recuperar = cliente.post(
        "/api/monitoreo/recuperar",
        json={"servicio": "backend-nodo-1"},
    )
    assert respuesta_recuperar.status_code == 200
    assert respuesta_recuperar.json()["estado"] == "ok"
    assert respuesta_recuperar.json()["resumen"]["caidos"] == 0
