import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './estilos/global.css'
import { ProveedorAuth } from './contextos/ContextoAuth'

ReactDOM.createRoot(document.getElementById('raiz')).render(
  <React.StrictMode>
    <ProveedorAuth>
      <App />
    </ProveedorAuth>
  </React.StrictMode>
)
