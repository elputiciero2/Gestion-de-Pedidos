import { useContext, useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ContextoAuth } from '../contextos/ContextoAuth'
import { actualizarEstadoPedido, eliminarPedido, obtenerPedido } from '../servicios/api'

const opcionesEstado = ['pendiente', 'en_proceso', 'enviado', 'entregado']

export default function DetallePedido() {
  const { id } = useParams()
  const { token, usuario } = useContext(ContextoAuth)
  const [pedido, setPedido] = useState(null)
  const [estadoSeleccionado, setEstadoSeleccionado] = useState('')
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')
  const navegar = useNavigate()
  const esAdmin = usuario?.rol === 'admin'

  const cargarPedido = async () => {
    try {
      const datos = await obtenerPedido(id, token)
      setPedido(datos)
      setEstadoSeleccionado(datos.estado)
    } catch (err) {
      setError(err.message || 'No se pudo cargar el pedido')
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    if (token) {
      cargarPedido()
    }
  }, [token, id])

  const manejarActualizarEstado = async (evento) => {
    evento.preventDefault()
    setError('')
    setExito('')
    try {
      const actualizado = await actualizarEstadoPedido(id, estadoSeleccionado, token)
      setPedido(actualizado)
      setExito('Estado actualizado correctamente')
    } catch (err) {
      setError(err.message || 'No se pudo actualizar el estado')
    }
  }

  const manejarEliminar = async () => {
    try {
      await eliminarPedido(id, token)
      navegar('/pedidos')
    } catch (err) {
      setError(err.message || 'No se pudo eliminar el pedido')
    }
  }

  if (cargando) {
    return <div className="cargando">Cargando pedido...</div>
  }

  if (!pedido) {
    return (
      <section className="seccion">
        <h1 className="titulo-seccion">Pedido no encontrado</h1>
      </section>
    )
  }

  return (
    <section className="seccion">
      <div className="fila" style={{ alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h1 className="titulo-seccion">Pedido #{pedido.id}</h1>
          <p>Creado: {new Date(pedido.creado_en).toLocaleString('es-ES')}</p>
        </div>
        {esAdmin && (
          <div className="acciones">
            <Link className="boton boton-secundario" to={`/pedidos/${pedido.id}/editar`}>
              Editar
            </Link>
            <button type="button" className="boton boton-peligro" onClick={manejarEliminar}>
              Eliminar
            </button>
          </div>
        )}
      </div>
      {error && <div className="mensaje-error">{error}</div>}
      {exito && <div className="mensaje-exito">{exito}</div>}
      <div className="tarjeta">
        <div className="fila">
          <div>
            <h3>Estado</h3>
            <span className={`estado-etiqueta estado-${pedido.estado}`}>{pedido.estado}</span>
          </div>
          <div>
            <h3>Dirección</h3>
            <p>{pedido.direccion_entrega}</p>
          </div>
          <div>
            <h3>Total</h3>
            <p>${pedido.total.toFixed(2)}</p>
          </div>
        </div>
      </div>
      {esAdmin && (
        <form className="formulario" onSubmit={manejarActualizarEstado}>
          <h3>Actualizar estado</h3>
          <div className="fila">
            <label className="campo">
              Nuevo estado
              <select
                value={estadoSeleccionado}
                onChange={(evento) => setEstadoSeleccionado(evento.target.value)}
              >
                {opcionesEstado.map((opcion) => (
                  <option key={opcion} value={opcion}>
                    {opcion.replace('_', ' ')}
                  </option>
                ))}
              </select>
            </label>
            <button type="submit" className="boton boton-primario">
              Guardar estado
            </button>
          </div>
        </form>
      )}
      <div className="tarjeta">
        <h3>Detalles</h3>
        <div className="detalle-lista">
          {pedido.detalles.map((detalle) => (
            <div className="detalle-item" key={detalle.id}>
              <div>
                <strong>{detalle.nombre_producto}</strong>
                <div>
                  {detalle.cantidad} x ${detalle.precio_unitario.toFixed(2)}
                </div>
              </div>
              <div>${detalle.subtotal.toFixed(2)}</div>
            </div>
          ))}
        </div>
      </div>
      <div className="resumen-total">Total: ${pedido.total.toFixed(2)}</div>
    </section>
  )
}
