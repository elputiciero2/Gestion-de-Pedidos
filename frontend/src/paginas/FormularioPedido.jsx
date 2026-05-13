import { useContext, useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ContextoAuth } from '../contextos/ContextoAuth'
import { actualizarPedido, crearPedido, obtenerPedido } from '../servicios/api'

const detalleVacio = {
  nombre_producto: '',
  cantidad: 1,
  precio_unitario: 0
}

const crearDetalle = (detalle = detalleVacio) => ({
  idLocal: crypto.randomUUID(),
  nombre_producto: detalle.nombre_producto,
  cantidad: detalle.cantidad,
  precio_unitario: detalle.precio_unitario
})

export default function FormularioPedido() {
  const { id } = useParams()
  const esEdicion = Boolean(id)
  const { token } = useContext(ContextoAuth)
  const [direccionEntrega, setDireccionEntrega] = useState('')
  const [detalles, setDetalles] = useState([crearDetalle()])
  const [cargando, setCargando] = useState(esEdicion)
  const [error, setError] = useState('')
  const navegar = useNavigate()

  useEffect(() => {
    const cargarPedido = async () => {
      try {
        const datos = await obtenerPedido(id, token)
        setDireccionEntrega(datos.direccion_entrega)
        setDetalles(
          datos.detalles.map((detalle) => ({
            idLocal: crypto.randomUUID(),
            nombre_producto: detalle.nombre_producto,
            cantidad: detalle.cantidad,
            precio_unitario: detalle.precio_unitario
          }))
        )
      } catch (err) {
        setError(err.message || 'No se pudo cargar el pedido')
      } finally {
        setCargando(false)
      }
    }

    if (esEdicion && token) {
      cargarPedido()
    }
  }, [esEdicion, id, token])

  const actualizarDetalle = (indice, campo, valor) => {
    setDetalles((previos) =>
      previos.map((detalle, posicion) =>
        posicion === indice ? { ...detalle, [campo]: valor } : detalle
      )
    )
  }

  const agregarDetalle = () => {
    setDetalles((previos) => [...previos, crearDetalle()])
  }

  const quitarDetalle = (indice) => {
    setDetalles((previos) => previos.filter((_, posicion) => posicion !== indice))
  }

  const manejarEnvio = async (evento) => {
    evento.preventDefault()
    setError('')
    if (!direccionEntrega.trim()) {
      setError('Ingresa una dirección de entrega')
      return
    }
    if (detalles.length === 0) {
      setError('Agrega al menos un producto')
      return
    }
    const payload = {
      direccion_entrega: direccionEntrega,
      detalles: detalles.map((detalle) => ({
        nombre_producto: detalle.nombre_producto,
        cantidad: Number(detalle.cantidad),
        precio_unitario: Number(detalle.precio_unitario)
      }))
    }

    try {
      const respuesta = esEdicion
        ? await actualizarPedido(id, payload, token)
        : await crearPedido(payload, token)
      navegar(`/pedidos/${respuesta.id}`)
    } catch (err) {
      setError(err.message || 'No se pudo guardar el pedido')
    }
  }

  if (cargando) {
    return <div className="cargando">Cargando formulario...</div>
  }

  return (
    <section className="seccion">
      <h1 className="titulo-seccion">{esEdicion ? 'Editar pedido' : 'Nuevo pedido'}</h1>
      {error && <div className="mensaje-error">{error}</div>}
      <form className="formulario" onSubmit={manejarEnvio}>
        <label className="campo">
          Dirección de entrega
          <input
            type="text"
            value={direccionEntrega}
            onChange={(evento) => setDireccionEntrega(evento.target.value)}
            placeholder="Calle 123, Ciudad"
            required
          />
        </label>
        <div className="seccion">
          <h3>Detalles del pedido</h3>
          {detalles.map((detalle, indice) => (
            <div className="tarjeta" key={detalle.idLocal}>
              <div className="fila">
                <label className="campo">
                  Producto
                  <input
                    type="text"
                    value={detalle.nombre_producto}
                    onChange={(evento) =>
                      actualizarDetalle(indice, 'nombre_producto', evento.target.value)
                    }
                    required
                  />
                </label>
                <label className="campo">
                  Cantidad
                  <input
                    type="number"
                    min="1"
                    value={detalle.cantidad}
                    onChange={(evento) =>
                      actualizarDetalle(indice, 'cantidad', evento.target.value)
                    }
                    required
                  />
                </label>
                <label className="campo">
                  Precio unitario
                  <input
                    type="number"
                    min="0.01"
                    step="0.01"
                    value={detalle.precio_unitario}
                    onChange={(evento) =>
                      actualizarDetalle(indice, 'precio_unitario', evento.target.value)
                    }
                    required
                  />
                </label>
              </div>
              {detalles.length > 1 && (
                <button
                  type="button"
                  className="boton boton-peligro"
                  onClick={() => quitarDetalle(indice)}
                >
                  Quitar detalle
                </button>
              )}
            </div>
          ))}
          <button type="button" className="boton boton-secundario" onClick={agregarDetalle}>
            Agregar producto
          </button>
        </div>
        <div className="acciones">
          <button type="submit" className="boton boton-primario">
            {esEdicion ? 'Actualizar pedido' : 'Crear pedido'}
          </button>
          <button type="button" className="boton boton-secundario" onClick={() => navegar('/pedidos')}>
            Cancelar
          </button>
        </div>
      </form>
    </section>
  )
}
