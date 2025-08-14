/**
 * Componente de Login
 * Archivo: LoginForm.jsx
 * Propósito: Formulario de autenticación con logo TZU y estilos profesionales
 * 
 * Características:
 * - Login con cualquier credencial (modo demo)
 * - Logo TZU con borde azul y sin fondo
 * - Gradiente de fondo moderno
 * - Botón de test para acceso directo
 * - Responsive y accesible
 */

import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import {
  loginContainerStyles,
  logoStyles,
  mainTitleStyles,
  formCardStyles,
  formContainerStyles,
  formSubtitleStyles,
  usernameInputStyles,
  passwordInputStyles,
  loginButtonStyles,
  helpTextStyles,
  testButtonStyles,
  getHoverEffects
} from '../styles/LoginStyles';

/**
 * Componente LoginForm
 * @param {Function} onLogin - Callback que se ejecuta cuando el usuario se autentica
 * @param {Function} setIsAuthenticated - Función para cambiar el estado de autenticación
 */
const LoginForm = ({ onLogin, setIsAuthenticated }) => {
  
  // Obtener efectos hover para los botones
  const hoverEffects = getHoverEffects();

  /**
   * Maneja el envío del formulario de login
   * @param {Event} e - Evento del formulario
   */
  const handleFormSubmit = (e) => {
    e.preventDefault();
    console.log('🚀 Login form submitted - authenticating user');
    
    // Guardar estado de autenticación en localStorage
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('username', 'admin');
    
    // Actualizar estado de React
    setIsAuthenticated(true);
    
    // Ejecutar callback si existe
    if (onLogin) {
      onLogin(true);
    }
  };

  /**
   * Maneja el login directo (botón de test)
   */
  const handleDirectLogin = () => {
    console.log('🧪 Test button - forcing authentication');
    
    // Guardar estado de autenticación en localStorage
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('username', 'test');
    
    // Actualizar estado de React
    setIsAuthenticated(true);
    
    // Ejecutar callback si existe
    if (onLogin) {
      onLogin(true);
    }
  };

  return (
    <ChakraProvider>
      {/* Contenedor principal con gradiente de fondo */}
      <div style={loginContainerStyles}>
        
        {/* Logo TZU con estilos profesionales */}
        <img 
          src="/tzu.png" 
          alt="TZU Logo" 
          style={logoStyles}
        />
        
        {/* Título principal */}
        <h1 style={mainTitleStyles}>
          🔐 TZU Security Login
        </h1>
        
        {/* Tarjeta del formulario */}
        <div style={formCardStyles}>
          <div style={formContainerStyles}>
            
            {/* Subtítulo del formulario */}
            <h2 style={formSubtitleStyles}>
              Ingreso al Sistema
            </h2>
            
            {/* Formulario de login */}
            <form onSubmit={handleFormSubmit}>
              
              {/* Campo de usuario */}
              <input 
                type="text" 
                placeholder="Usuario" 
                style={usernameInputStyles}
                autoComplete="username"
              />
              
              {/* Campo de contraseña */}
              <input 
                type="password" 
                placeholder="Contraseña" 
                style={passwordInputStyles}
                autoComplete="current-password"
              />
              
              {/* Botón principal de login */}
              <button 
                type="submit" 
                style={loginButtonStyles}
                onMouseOver={hoverEffects.loginButton.onMouseOver}
                onMouseOut={hoverEffects.loginButton.onMouseOut}
              >
                🔑 Ingresar
              </button>
              
            </form>
            
            {/* Texto de ayuda */}
            <p style={helpTextStyles}>
              Cualquier usuario/contraseña es válida para demo
            </p>
            
            {/* Botón de test para desarrollo */}
            <button 
              onClick={handleDirectLogin}
              style={testButtonStyles}
            >
              🧪 Login directo (Test)
            </button>
            
          </div>
        </div>
      </div>
    </ChakraProvider>
  );
};

export default LoginForm;
