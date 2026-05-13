import { useContext } from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { ContextoAuth } from '../contextos/ContextoAuth'

export default function RutaProtegida({ rolesPermitidos }) {
  const { usuario, token, cargando } = useContext(ContextoAuth)

  if (cargando) {
    return <div className="cargando">Cargando...</div>
  }

  if (!token || !usuario) {
    return <Navigate to="/login" replace />
  }

  if (rolesPermitidos && !rolesPermitidos.includes(usuario.rol)) {
    return <Navigate to="/no-encontrado" replace />
  }

  return <Outlet />
}
