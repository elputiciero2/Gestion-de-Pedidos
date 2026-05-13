import { Link } from 'react-router-dom'

export default function NoEncontrado() {
  return (
    <section className="seccion" style={{ textAlign: 'center', padding: '3rem 1.5rem' }}>
      <h1 className="titulo-seccion">Página no encontrada</h1>
      <p>La ruta que buscas no existe o no tienes permisos.</p>
      <div style={{ marginTop: '1.5rem' }}>
        <Link to="/" className="boton boton-primario">
          Volver al inicio
        </Link>
      </div>
    </section>
  )
}
