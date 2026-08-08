import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { ThemeProvider } from './ThemeProvider.jsx'
import { MainRoutes } from './MainRoutes.jsx'
import { AuthProvider } from './AuthProvider.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <MainRoutes />
      </AuthProvider>
    </ThemeProvider>
  </StrictMode>,
)
