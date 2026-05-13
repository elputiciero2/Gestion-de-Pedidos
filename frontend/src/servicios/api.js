const URL_BASE = import.meta.env.VITE_API_URL || ''

const construirUrl = (ruta) => `${URL_BASE}${ruta}`

const leerRespuesta = async (respuesta) => {
  if (respuesta.status === 204) {
    return null
  }
  const tipo = respuesta.headers.get('content-type') || ''
  if (tipo.includes('application/json')) {
    return await respuesta.json()
  }
  const texto = await respuesta.text()
  return texto ? { mensaje: texto } : null
}

const solicitud = async (ruta, opciones = {}, token) => {
  const encabezados = {
    'Content-Type': 'application/json',
    ...(opciones.headers || {})
  }
  if (token) {
    encabezados.Authorization = `Bearer ${token}`
  }
  const respuesta = await fetch(construirUrl(ruta), {
    ...opciones,
    headers: encabezados
  })
  const datos = await leerRespuesta(respuesta)
  if (!respuesta.ok) {
    const mensaje = datos?.detail || datos?.mensaje || 'Error en la solicitud'
    const error = new Error(mensaje)
    error.estado = respuesta.status
    throw error
  }
  return datos
}

export const registrarUsuario = (datos) =>
  solicitud('/api/autenticacion/registro', {
    method: 'POST',
    body: JSON.stringify(datos)
  })

export const iniciarSesion = (credenciales) =>
  solicitud('/api/autenticacion/login', {
    method: 'POST',
    body: JSON.stringify(credenciales)
  })

export const obtenerUsuarioActual = (token) => solicitud('/api/autenticacion/me', {}, token)

export const listarPedidos = (token) => solicitud('/api/pedidos', {}, token)

export const obtenerPedido = (id, token) => solicitud(`/api/pedidos/${id}`, {}, token)

export const crearPedido = (datos, token) =>
  solicitud('/api/pedidos', {
    method: 'POST',
    body: JSON.stringify(datos)
  }, token)

export const actualizarPedido = (id, datos, token) =>
  solicitud(`/api/pedidos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(datos)
  }, token)

export const eliminarPedido = (id, token) =>
  solicitud(`/api/pedidos/${id}`, {
    method: 'DELETE'
  }, token)

export const actualizarEstadoPedido = (id, estado, token) =>
  solicitud(`/api/pedidos/${id}/estado`, {
    method: 'PATCH',
    body: JSON.stringify({ estado })
  }, token)

export const obtenerSalud = () => solicitud('/api/salud')

export const obtenerSaludDetalle = () => solicitud('/api/salud/detalle')

export const obtenerMonitoreoEstado = () => solicitud('/api/monitoreo/estado')

export const simularFalla = ({ servicio, detalle } = {}) =>
  solicitud('/api/monitoreo/falla', {
    method: 'POST',
    body: JSON.stringify({
      servicio: servicio || 'backend-nodo-1',
      detalle: detalle || null
    })
  })

export const recuperarMonitoreo = ({ servicio } = {}) =>
  solicitud('/api/monitoreo/recuperar', {
    method: 'POST',
    body: JSON.stringify({
      servicio: servicio || null
    })
  })
