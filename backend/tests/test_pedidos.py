
def registrar_y_obtener_token(cliente, correo: str, rol: str = "usuario") -> str:
    cliente.post(
        "/api/autenticacion/registro",
        json={"nombre": "Juan", "correo": correo, "clave": "clave123", "rol": rol},
    )
    respuesta_login = cliente.post(
        "/api/autenticacion/login",
        json={"correo": correo, "clave": "clave123"},
    )
    return respuesta_login.json()["token_acceso"]


def test_crud_pedidos_y_transiciones(cliente):
    token = registrar_y_obtener_token(cliente, "juan@example.com", rol="admin")
    encabezados = {"Authorization": f"Bearer {token}"}

    respuesta_crear = cliente.post(
        "/api/pedidos",
        headers=encabezados,
        json={
            "direccion_entrega": "Calle 123",
            "detalles": [
                {"nombre_producto": "Producto A", "cantidad": 2, "precio_unitario": 10.0},
                {"nombre_producto": "Producto B", "cantidad": 1, "precio_unitario": 5.5},
            ],
        },
    )
    assert respuesta_crear.status_code == 201
    pedido = respuesta_crear.json()
    assert pedido["estado"] == "pendiente"
    pedido_id = pedido["id"]

    respuesta_listar = cliente.get("/api/pedidos", headers=encabezados)
    assert respuesta_listar.status_code == 200
    assert len(respuesta_listar.json()) == 1

    respuesta_actualizar = cliente.put(
        f"/api/pedidos/{pedido_id}",
        headers=encabezados,
        json={
            "direccion_entrega": "Calle 456",
            "detalles": [
                {"nombre_producto": "Producto C", "cantidad": 3, "precio_unitario": 4.0},
            ],
        },
    )
    assert respuesta_actualizar.status_code == 200
    assert respuesta_actualizar.json()["direccion_entrega"] == "Calle 456"

    respuesta_estado = cliente.patch(
        f"/api/pedidos/{pedido_id}/estado",
        headers=encabezados,
        json={"estado": "en_proceso"},
    )
    assert respuesta_estado.status_code == 200
    assert respuesta_estado.json()["estado"] == "en_proceso"

    respuesta_estado_invalida = cliente.patch(
        f"/api/pedidos/{pedido_id}/estado",
        headers=encabezados,
        json={"estado": "pendiente"},
    )
    assert respuesta_estado_invalida.status_code == 400

    respuesta_estado = cliente.patch(
        f"/api/pedidos/{pedido_id}/estado",
        headers=encabezados,
        json={"estado": "enviado"},
    )
    assert respuesta_estado.status_code == 200

    respuesta_estado = cliente.patch(
        f"/api/pedidos/{pedido_id}/estado",
        headers=encabezados,
        json={"estado": "entregado"},
    )
    assert respuesta_estado.status_code == 200

    respuesta_eliminar = cliente.delete(f"/api/pedidos/{pedido_id}", headers=encabezados)
    assert respuesta_eliminar.status_code == 204

    respuesta_obtener = cliente.get(f"/api/pedidos/{pedido_id}", headers=encabezados)
    assert respuesta_obtener.status_code == 404


def test_usuario_normal_solo_lectura(cliente):
    token = registrar_y_obtener_token(cliente, "lectura@example.com")
    encabezados = {"Authorization": f"Bearer {token}"}

    respuesta_crear = cliente.post(
        "/api/pedidos",
        headers=encabezados,
        json={
            "direccion_entrega": "Calle 999",
            "detalles": [
                {"nombre_producto": "Producto X", "cantidad": 1, "precio_unitario": 10.0},
            ],
        },
    )
    assert respuesta_crear.status_code == 403

    respuesta_listar = cliente.get("/api/pedidos", headers=encabezados)
    assert respuesta_listar.status_code == 200
