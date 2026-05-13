def test_salud_ok(cliente):
    respuesta = cliente.get("/api/salud")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "ok"


def test_salud_detalle(cliente):
    respuesta = cliente.get("/api/salud/detalle")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "ok"
