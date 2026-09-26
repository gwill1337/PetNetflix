import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
// import App from './App.tsx'
import { ThemeProvider } from './components/ThemeProvider.tsx'
import { MainRoutes } from './MainRoutes.tsx'
import { AuthProvider } from './components/AuthProvider.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <MainRoutes />
      </AuthProvider>
    </ThemeProvider>
  </StrictMode>,
)
