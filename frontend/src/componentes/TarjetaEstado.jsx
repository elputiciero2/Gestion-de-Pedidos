export default function TarjetaEstado({ titulo, valor, descripcion, estado }) {
  const claseEstado = estado ? `estado-${estado}` : ''

  return (
    <article className="tarjeta">
      <div className="tarjeta-encabezado">
        <h3>{titulo}</h3>
        <span className={`indicador ${claseEstado}`}>{valor}</span>
      </div>
      <p>{descripcion}</p>
    </article>
  )
}
