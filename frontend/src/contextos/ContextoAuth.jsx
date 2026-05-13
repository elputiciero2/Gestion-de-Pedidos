import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { iniciarSesion as iniciarSesionApi, obtenerUsuarioActual } from '../servicios/api'

const CLAVE_TOKEN = 'token_acceso'

export const ContextoAuth = createContext(null)

export function ProveedorAuth({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(CLAVE_TOKEN))
  const [usuario, setUsuario] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)

  const limpiarSesion = () => {
    localStorage.removeItem(CLAVE_TOKEN)
    setToken(null)
    setUsuario(null)
  }

  const cargarUsuario = async (tokenActual) => {
    try {
      const usuarioActual = await obtenerUsuarioActual(tokenActual)
      setUsuario(usuarioActual)
      setToken(tokenActual)
    } catch (err) {
      limpiarSesion()
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    const tokenGuardado = localStorage.getItem(CLAVE_TOKEN)
    if (!tokenGuardado) {
      setCargando(false)
      return
    }
    cargarUsuario(tokenGuardado)
  }, [])

  const iniciarSesion = async (credenciales) => {
    setError(null)
    const datos = await iniciarSesionApi(credenciales)
    const tokenNuevo = datos.token_acceso
    localStorage.setItem(CLAVE_TOKEN, tokenNuevo)
    setToken(tokenNuevo)
    const usuarioActual = await obtenerUsuarioActual(tokenNuevo)
    setUsuario(usuarioActual)
    return usuarioActual
  }

  const cerrarSesion = () => {
    limpiarSesion()
  }

  const valor = useMemo(
    () => ({ token, usuario, cargando, error, iniciarSesion, cerrarSesion, setError }),
    [token, usuario, cargando, error]
  )

  return <ContextoAuth.Provider value={valor}>{children}</ContextoAuth.Provider>
}

export const usarAuth = () => useContext(ContextoAuth)
