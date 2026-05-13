import { useContext, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ContextoAuth } from '../contextos/ContextoAuth'
import { registrarUsuario } from '../servicios/api'

export default function Login() {
  const { iniciarSesion } = useContext(ContextoAuth)
  const [modo, setModo] = useState('login')
  const [nombre, setNombre] = useState('')
  const [correo, setCorreo] = useState('')
  const [clave, setClave] = useState('')
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')
  const navegar = useNavigate()

  const manejarEnvio = async (evento) => {
    evento.preventDefault()
    setCargando(true)
    setError('')
    setExito('')
    try {
      if (modo === 'registro') {
        await registrarUsuario({
          nombre,
          correo,
          clave
        })
        setExito('Usuario creado. Ahora puedes iniciar sesión.')
        setModo('login')
        setNombre('')
      } else {
        await iniciarSesion({ correo, clave })
        navegar('/')
      }
    } catch (err) {
      setError(err.message || 'No fue posible completar la operación')
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="contenido-principal">
      <section className="seccion" style={{ maxWidth: '520px', margin: '0 auto' }}>
        <div className="cabecera-seccion">
          <h1 className="titulo-seccion">
            {modo === 'login' ? 'Iniciar sesión' : 'Registrarte'}
          </h1>
          <p>
            {modo === 'login'
              ? 'Entra con tu correo y clave. Si todavía no tienes cuenta, puedes crearla aquí mismo.'
              : 'Crea un usuario normal para consultar pedidos y operar dentro de la plataforma.'}
          </p>
        </div>
        {error && <div className="mensaje-error">{error}</div>}
        {exito && <div className="mensaje-exito">{exito}</div>}
        <form className="formulario" onSubmit={manejarEnvio}>
          {modo === 'registro' && (
            <label className="campo">
              Nombre
              <input
                type="text"
                value={nombre}
                onChange={(evento) => setNombre(evento.target.value)}
                placeholder="Tu nombre"
                required
              />
            </label>
          )}
          <label className="campo">
            Correo
            <input
              type="email"
              value={correo}
              onChange={(evento) => setCorreo(evento.target.value)}
              placeholder="usuario@correo.com"
              required
            />
          </label>
          <label className="campo">
            Clave
            <input
              type="password"
              value={clave}
              onChange={(evento) => setClave(evento.target.value)}
              placeholder="••••••••"
              required
            />
          </label>
          <button type="submit" className="boton boton-primario" disabled={cargando}>
            {cargando ? 'Procesando...' : modo === 'login' ? 'Entrar' : 'Crear usuario'}
          </button>
          <button
            type="button"
            className="boton boton-secundario"
            onClick={() => {
              setError('')
              setExito('')
              setModo((valor) => (valor === 'login' ? 'registro' : 'login'))
            }}
          >
            {modo === 'login' ? 'Registrarte' : 'Volver a iniciar sesión'}
          </button>
        </form>
      </section>
    </div>
  )
}
