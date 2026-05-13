import { useContext, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ContextoAuth } from '../contextos/ContextoAuth'
import { eliminarPedido, listarPedidos } from '../servicios/api'

const formatearEstado = (estado) => estado.replace('_', ' ')

export default function ListaPedidos() {
  const { token, usuario } = useContext(ContextoAuth)
  const navigate = useNavigate()
  const [pedidos, setPedidos] = useState([])
  const [pedidoIdBusqueda, setPedidoIdBusqueda] = useState('')
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  const cargarPedidos = async () => {
    try {
      const datos = await listarPedidos(token)
      setPedidos(datos || [])
    } catch (err) {
      setError(err.message || 'No se pudieron cargar los pedidos')
    } finally {
      setCargando(false)
    }
  }

  const buscarPedido = async () => {
    const idNormalizado = pedidoIdBusqueda.trim()
    if (!idNormalizado) {
      setError('Ingresa un ID de pedido')
      return
    }
    navigate(`/pedidos/${idNormalizado}`)
  }

  const verTodos = async () => {
    setCargando(true)
    setError('')
    await cargarPedidos()
    setPedidoIdBusqueda('')
  }

  useEffect(() => {
    if (token) {
      cargarPedidos()
    }
  }, [token])

  const manejarEliminar = async (id) => {
    try {
      await eliminarPedido(id, token)
      setPedidos((previos) => previos.filter((pedido) => pedido.id !== id))
    } catch (err) {
      setError(err.message || 'No se pudo eliminar el pedido')
    }
  }

  if (cargando) {
    return <div className="cargando">Cargando pedidos...</div>
  }

  return (
    <section className="seccion">
      <div className="cabecera-seccion">
        <h1 className="titulo-seccion">Pedidos</h1>
        <p>Busca por ID, revisa un pedido puntual o lista todo lo que existe.</p>
      </div>
      <div className="tarjeta">
        <div className="fila">
          <label className="campo">
            Buscar por ID
            <input
              type="number"
              min="1"
              value={pedidoIdBusqueda}
              onChange={(evento) => setPedidoIdBusqueda(evento.target.value)}
              placeholder="Ej. 15"
            />
          </label>
          <div className="acciones">
            <button type="button" className="boton boton-primario" onClick={buscarPedido}>
              Ver pedido
            </button>
            <button type="button" className="boton boton-secundario" onClick={verTodos}>
              Ver todos
            </button>
            {usuario?.rol === 'admin' && (
              <Link className="boton boton-primario" to="/pedidos/nuevo">
                Nuevo pedido
              </Link>
            )}
          </div>
        </div>
      </div>
      {error && <div className="mensaje-error">{error}</div>}
      {pedidos.length === 0 ? (
        <div className="tarjeta">
          <p>No hay pedidos registrados.</p>
        </div>
      ) : (
        <div className="tabla-responsiva">
          <table className="tabla">
            <thead>
              <tr>
                <th>ID</th>
                <th>Estado</th>
                <th>Total</th>
                <th>Creado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {pedidos.map((pedido) => (
                <tr key={pedido.id}>
                  <td>#{pedido.id}</td>
                  <td>
                    <span className={`estado-etiqueta estado-${pedido.estado}`}>
                      {formatearEstado(pedido.estado)}
                    </span>
                  </td>
                  <td>${pedido.total.toFixed(2)}</td>
                  <td>{new Date(pedido.creado_en).toLocaleString('es-ES')}</td>
                  <td>
                    <div className="acciones">
                      <Link className="boton boton-secundario" to={`/pedidos/${pedido.id}`}>
                        Ver
                      </Link>
                      {usuario?.rol === 'admin' && (
                        <>
                          <Link
                            className="boton boton-secundario"
                            to={`/pedidos/${pedido.id}/editar`}
                          >
                            Editar
                          </Link>
                          <button
                            type="button"
                            className="boton boton-peligro"
                            onClick={() => manejarEliminar(pedido.id)}
                          >
                            Eliminar
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
