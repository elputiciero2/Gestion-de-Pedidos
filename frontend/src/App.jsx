import { BrowserRouter, Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { useContext } from 'react'
import { ContextoAuth } from './contextos/ContextoAuth'
import BarraNavegacion from './componentes/BarraNavegacion'
import RutaProtegida from './componentes/RutaProtegida'
import Login from './paginas/Login'
import ListaPedidos from './paginas/ListaPedidos'
import DetallePedido from './paginas/DetallePedido'
import FormularioPedido from './paginas/FormularioPedido'
import Dashboard from './paginas/Dashboard'
import NoEncontrado from './paginas/NoEncontrado'

function DisenoAutenticado() {
  return (
    <div className="contenedor-app">
      <BarraNavegacion />
      <main className="contenido-principal">
        <Outlet />
      </main>
    </div>
  )
}

function Inicio() {
  const { usuario, cargando } = useContext(ContextoAuth)

  if (cargando) {
    return <div className="cargando">Cargando...</div>
  }

  if (usuario?.rol === 'admin') {
    return <Navigate to="/dashboard" replace />
  }

  return <Navigate to="/pedidos" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<RutaProtegida />}>
          <Route element={<DisenoAutenticado />}>
            <Route index element={<Inicio />} />
            <Route path="pedidos" element={<ListaPedidos />} />
            <Route path="pedidos/:id" element={<DetallePedido />} />
            <Route element={<RutaProtegida rolesPermitidos={["admin"]} />}>
              <Route path="pedidos/nuevo" element={<FormularioPedido />} />
              <Route path="pedidos/:id/editar" element={<FormularioPedido />} />
              <Route path="dashboard" element={<Dashboard />} />
            </Route>
          </Route>
        </Route>
        <Route path="/no-encontrado" element={<NoEncontrado />} />
        <Route path="*" element={<NoEncontrado />} />
      </Routes>
    </BrowserRouter>
  )
}
