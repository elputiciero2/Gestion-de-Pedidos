class CircuitBreaker {
  constructor(umbralFallos = 3, tiempoReintento = 30000) {
    this.estado = 'CERRADO'
    this.contadorFallos = 0
    this.umbralFallos = umbralFallos
    this.tiempoReintento = tiempoReintento
    this.timestampApertura = null
  }

  registrarFallo() {
    this.contadorFallos++
    if (this.contadorFallos >= this.umbralFallos) {
      this.estado = 'ABIERTO'
      this.timestampApertura = Date.now()
    }
  }

  registrarExito() {
    this.contadorFallos = 0
    this.estado = 'CERRADO'
  }

  puedeIntentarAhora() {
    if (this.estado === 'CERRADO') {
      return true
    }
    if (this.estado === 'ABIERTO') {
      const tiempoTranscurrido = Date.now() - this.timestampApertura
      if (tiempoTranscurrido >= this.tiempoReintento) {
        this.estado = 'SEMI_ABIERTO'
        return true
      }
      return false
    }
    return this.estado === 'SEMI_ABIERTO'
  }

  obtenerEstado() {
    return this.estado
  }
}

class RetryManager {
  constructor(maxReintentos = Infinity) {
    this.intentos = 0
    this.maxReintentos = maxReintentos
  }

  calcularDelay(numeroIntento) {
    if (numeroIntento >= 5) {
      return 60000
    }
    const delayMs = Math.pow(2, numeroIntento) * 1000
    return Math.min(delayMs, 60000)
  }

  registrarIntento() {
    this.intentos++
  }

  registrarExito() {
    this.intentos = 0
  }

  obtenerIntentos() {
    return this.intentos
  }

  hayIntentosPendientes() {
    return true
  }
}

const circuitBreaker = new CircuitBreaker(3, 30000)
const retryManager = new RetryManager()

async function realizarLlamadaConReintentos(url, opciones = {}) {
  if (!circuitBreaker.puedeIntentarAhora()) {
    throw new Error(`Circuit breaker abierto. Reintentando en ${30}s`)
  }

  try {
    const respuesta = await fetch(url, opciones)
    
    if (!respuesta.ok && respuesta.status >= 500) {
      throw new Error(`Error del servidor: ${respuesta.status}`)
    }
    
    circuitBreaker.registrarExito()
    retryManager.registrarExito()
    
    return respuesta
  } catch (error) {
    const delay = retryManager.calcularDelay(retryManager.obtenerIntentos())
    retryManager.registrarIntento()
    
    console.log(`Reintentando en ${delay}ms (intento ${retryManager.obtenerIntentos()} de ∞)`)
    
    circuitBreaker.registrarFallo()
    
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        realizarLlamadaConReintentos(url, opciones)
          .then(resolve)
          .catch(reject)
      }, delay)
    })
  }
}

const URL_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || ''

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

export { CircuitBreaker, RetryManager, realizarLlamadaConReintentos }
