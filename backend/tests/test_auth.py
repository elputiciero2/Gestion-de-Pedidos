from app.configuracion import obtener_configuracion


def test_admin_precargado_puede_iniciar_sesion(cliente):
    configuracion = obtener_configuracion()

    respuesta_login = cliente.post(
        "/api/autenticacion/login",
        json={
            "correo": configuracion.admin_correo,
            "clave": configuracion.admin_clave,
        },
    )
    assert respuesta_login.status_code == 200
    datos_login = respuesta_login.json()
    assert datos_login["tipo"] == "bearer"

    respuesta_me = cliente.get(
        "/api/autenticacion/me",
        headers={"Authorization": f"Bearer {datos_login['token_acceso']}"},
    )
    assert respuesta_me.status_code == 200
    datos_me = respuesta_me.json()
    assert datos_me["correo"] == configuracion.admin_correo
    assert datos_me["rol"] == "admin"


def test_registro_login_me(cliente):
    respuesta_registro = cliente.post(
        "/api/autenticacion/registro",
        json={"nombre": "Ana", "correo": "ana@example.com", "clave": "clave123"},
    )
    assert respuesta_registro.status_code == 201
    datos_registro = respuesta_registro.json()
    assert datos_registro["correo"] == "ana@example.com"

    respuesta_login = cliente.post(
        "/api/autenticacion/login",
        json={"correo": "ana@example.com", "clave": "clave123"},
    )
    assert respuesta_login.status_code == 200
    token = respuesta_login.json()["token_acceso"]

    respuesta_me = cliente.get(
        "/api/autenticacion/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert respuesta_me.status_code == 200
    datos_me = respuesta_me.json()
    assert datos_me["correo"] == "ana@example.com"
