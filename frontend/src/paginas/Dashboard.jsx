import { useEffect, useState } from 'react'
import {
  obtenerMonitoreoEstado,
  obtenerSalud,
  obtenerSaludDetalle,
  recuperarMonitoreo,
  simularFalla
} from '../servicios/api'
import TarjetaEstado from '../componentes/TarjetaEstado'

export default function Dashboard() {
  const [salud, setSalud] = useState(null)
  const [saludDetalle, setSaludDetalle] = useState(null)
  const [monitoreo, setMonitoreo] = useState(null)
  const [detalleFalla, setDetalleFalla] = useState('')
  const [servicioSeleccionado, setServicioSeleccionado] = useState('backend-nodo-1')
  const [erroresCarga, setErroresCarga] = useState([])
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  const cargarEstado = async () => {
    setError('')
    const resultados = await Promise.allSettled([
      obtenerSalud(),
      obtenerSaludDetalle(),
      obtenerMonitoreoEstado()
    ])
    const errores = []
    const [saludResultado, detalleResultado, monitoreoResultado] = resultados

    if (saludResultado.status === 'fulfilled') {
      setSalud(saludResultado.value)
    } else {
      errores.push({
        modulo: 'Salud API',
        mensaje: saludResultado.reason?.message || 'No respondió el endpoint de salud.'
      })
    }

    if (detalleResultado.status === 'fulfilled') {
      setSaludDetalle(detalleResultado.value)
    } else {
      errores.push({
        modulo: 'Salud detallada',
        mensaje: detalleResultado.reason?.message || 'No respondió el endpoint de detalle.'
      })
    }

    if (monitoreoResultado.status === 'fulfilled') {
      setMonitoreo(monitoreoResultado.value)
    } else {
      errores.push({
        modulo: 'Monitoreo',
        mensaje: monitoreoResultado.reason?.message || 'No respondió el endpoint de monitoreo.'
      })
    }

    setErroresCarga(errores)
    if (errores.length > 0) {
      setError('Hay módulos del dashboard que no respondieron. Revisa el detalle de errores.')
    }
  }

  useEffect(() => {
    cargarEstado()
    const intervalo = setInterval(cargarEstado, 5000)
    return () => clearInterval(intervalo)
  }, [])

  const manejarFalla = async () => {
    setError('')
    setMensaje('')
    try {
      const respuesta = await simularFalla({
        servicio: servicioSeleccionado,
        detalle: detalleFalla
      })
      setMonitoreo(respuesta)
      setMensaje('Falla simulada correctamente')
      setDetalleFalla('')
    } catch (err) {
      setError(err.message || 'No se pudo simular la falla')
    }
  }

  const manejarRecuperacion = async () => {
    setError('')
    setMensaje('')
    try {
      const respuesta = await recuperarMonitoreo({
        servicio: servicioSeleccionado
      })
      setMonitoreo(respuesta)
      setMensaje('Recuperación ejecutada')
    } catch (err) {
      setError(err.message || 'No se pudo recuperar el nodo')
    }
  }

  return (
    <section className="seccion">
      <div className="cabecera-seccion">
        <h1 className="titulo-seccion">Dashboard de monitoreo</h1>
        <p>
          Supervisa el estado del sistema, identifica el servicio caído y sigue el detalle de
          recuperación sin abandonar la vista.
        </p>
      </div>
      {error && <div className="mensaje-error">{error}</div>}
      {mensaje && <div className="mensaje-exito">{mensaje}</div>}
      {erroresCarga.length > 0 && (
        <div className="tarjeta tarjeta-alerta">
          <h3>Errores de carga</h3>
          <div className="lista-alertas">
            {erroresCarga.map((item) => (
              <article key={item.modulo} className="alerta-item">
                <strong>{item.modulo}</strong>
                <span>{item.mensaje}</span>
              </article>
            ))}
          </div>
        </div>
      )}
      <div className="tarjetas-grid">
        <TarjetaEstado
          titulo="Salud general"
          valor={salud?.estado || '...'}
          descripcion={saludDetalle?.detalle || 'Sin información'}
          estado={salud?.estado === 'ok' ? 'ok' : 'alerta'}
        />
        <TarjetaEstado
          titulo="Servicios operativos"
          valor={monitoreo?.resumen ? `${monitoreo.resumen.operativos}/${monitoreo.resumen.total}` : '...'}
          descripcion="Cantidad de servicios funcionando dentro del stack."
          estado={monitoreo?.resumen?.caidos ? 'falla' : 'ok'}
        />
        <TarjetaEstado
          titulo="Incidencia activa"
          valor={monitoreo?.incidencia_actual ? 'Sí' : 'No'}
          descripcion={monitoreo?.incidencia_actual?.detalle || 'No hay incidentes abiertos'}
          estado={monitoreo?.estado === 'ok' ? 'ok' : 'falla'}
        />
        <TarjetaEstado
          titulo="Actualización"
          valor={saludDetalle?.actualizado_en ? 'Reciente' : '...'}
          descripcion={saludDetalle?.actualizado_en || 'Sin marca temporal'}
          estado="ok"
        />
      </div>
      <div className="tarjeta">
        <div className="tarjeta-encabezado">
          <h3>Simular y recuperar incidentes</h3>
          <span className="estado-etiqueta estado-pendiente">Operación admin</span>
        </div>
        <div className="fila">
          <label className="campo">
            Servicio afectado
            <select value={servicioSeleccionado} onChange={(evento) => setServicioSeleccionado(evento.target.value)}>
              {(monitoreo?.servicios || [
                { nombre: 'backend-nodo-1', tipo: 'api' },
                { nombre: 'backend-nodo-2', tipo: 'api' },
                { nombre: 'mysql-nodo-1', tipo: 'base_datos' },
                { nombre: 'mysql-nodo-2', tipo: 'base_datos' },
                { nombre: 'mysql-nodo-3', tipo: 'base_datos' },
                { nombre: 'nginx', tipo: 'proxy' },
                { nombre: 'phpmyadmin', tipo: 'herramienta' }
              ]).map((servicio) => (
                <option key={servicio.nombre} value={servicio.nombre}>
                  {servicio.nombre} · {servicio.tipo}
                </option>
              ))}
            </select>
          </label>
          <label className="campo">
            Detalle del incidente
            <input
              type="text"
              value={detalleFalla}
              onChange={(evento) => setDetalleFalla(evento.target.value)}
              placeholder="Interrupción en el backend 1"
            />
          </label>
        </div>
        <div className="acciones">
          <button type="button" className="boton boton-peligro" onClick={manejarFalla}>
            Simular falla
          </button>
          <button type="button" className="boton boton-secundario" onClick={manejarRecuperacion}>
            Recuperar servicio
          </button>
        </div>
      </div>
      <div className="tarjeta">
        <div className="tarjeta-encabezado">
          <h3>Cómo se está comportando el sistema</h3>
          <span className={`estado-etiqueta ${monitoreo?.estado === 'falla' ? 'estado-falla' : 'estado-ok'}`}>
            {monitoreo?.estado || '...'}
          </span>
        </div>
        <p>{monitoreo?.detalle || 'Sin diagnóstico disponible todavía.'}</p>
        <div className="panel-metricas">
          <div>
            <strong>Total de servicios</strong>
            <span>{monitoreo?.resumen?.total ?? '...'}</span>
          </div>
          <div>
            <strong>Operativos</strong>
            <span>{monitoreo?.resumen?.operativos ?? '...'}</span>
          </div>
          <div>
            <strong>Caídos</strong>
            <span>{monitoreo?.resumen?.caidos ?? '...'}</span>
          </div>
        </div>
      </div>
      <div className="tarjeta">
        <div className="tarjeta-encabezado">
          <h3>Última incidencia</h3>
          <span className="estado-etiqueta estado-alerta">
            {monitoreo?.ultima_incidencia?.estado || 'sin cambios'}
          </span>
        </div>
        <pre className="bloque-detalle">
{JSON.stringify(monitoreo?.ultima_incidencia || monitoreo?.incidencia_actual || { mensaje: 'Sin incidente reciente' }, null, 2)}
        </pre>
      </div>
      <div className="tarjeta">
        <h3>Mapa de servicios</h3>
        <div className="tabla-monitoreo">
          {(monitoreo?.servicios || []).map((servicio) => (
            <article key={servicio.nombre} className="fila-servicio">
              <div>
                <strong>{servicio.nombre}</strong>
                <p>{servicio.tipo}</p>
              </div>
              <span className={`estado-etiqueta estado-${servicio.estado}`}>
                {servicio.estado}
              </span>
              <div className="texto-mono">{servicio.ruta}</div>
              <div className="texto-mono">{servicio.detalle}</div>
              <div className="texto-mono">{servicio.ultimo_evento}</div>
            </article>
          ))}
        </div>
      </div>
      <div className="tarjeta">
        <h3>Recomendaciones de operación</h3>
        <ul className="lista-operativa">
          {(monitoreo?.recomendaciones || []).map((recomendacion) => (
            <li key={recomendacion}>{recomendacion}</li>
          ))}
        </ul>
      </div>
    </section>
  )
}
