import { NavLink, useNavigate } from 'react-router-dom'
import { useContext, useState } from 'react'
import { ContextoAuth } from '../contextos/ContextoAuth'

export default function BarraNavegacion() {
  const { usuario, cerrarSesion } = useContext(ContextoAuth)
  const [menuAbierto, setMenuAbierto] = useState(false)
  const navegar = useNavigate()

  const claseEnlace = ({ isActive }) =>
    `menu-enlace${isActive ? ' activo' : ''}`

  const manejarCerrarSesion = () => {
    cerrarSesion()
    navegar('/login')
  }

  return (
    <header className="barra-navegacion">
      <div className="barra-contenido">
        <span className="marca">Gestión de Pedidos</span>
        <nav className="menu">
          <div className={`menu-enlaces${menuAbierto ? ' abierto' : ''}`}>
            <NavLink to="/pedidos" className={claseEnlace} onClick={() => setMenuAbierto(false)}>
              Pedidos
            </NavLink>
            {usuario?.rol === 'admin' && (
              <>
                <NavLink
                  to="/pedidos/nuevo"
                  className={claseEnlace}
                  onClick={() => setMenuAbierto(false)}
                >
                  Nuevo pedido
                </NavLink>
                <NavLink
                  to="/dashboard"
                  className={claseEnlace}
                  onClick={() => setMenuAbierto(false)}
                >
                  Dashboard
                </NavLink>
              </>
            )}
          </div>
          <span className="usuario-info">
            {usuario ? `${usuario.nombre} (${usuario.rol})` : ''}
          </span>
          <button
            type="button"
            className="boton boton-ghost"
            onClick={manejarCerrarSesion}
          >
            Salir
          </button>
          <button
            type="button"
            className="menu-boton"
            onClick={() => setMenuAbierto((valor) => !valor)}
          >
            Menú
          </button>
        </nav>
      </div>
    </header>
  )
}
