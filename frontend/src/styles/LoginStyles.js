/**
 * Estilos centralizados para el sistema de login
 * Archivo: LoginStyles.js
 * Propósito: Contener todos los estilos del login en un lugar centralizado
 */

// Estilos para el contenedor principal del login
export const loginContainerStyles = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  flexDirection: 'column',
  gap: '30px'
};

// Estilos para el logo TZU
export const logoStyles = {
  width: '180px',
  height: 'auto',
  filter: 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2))',
  backgroundColor: 'transparent',
  borderRadius: '50%',
  padding: '15px',
  border: '3px solid rgba(59, 130, 246, 0.8)',
  backdropFilter: 'blur(5px)'
};

// Estilos para el título principal
export const mainTitleStyles = {
  color: 'white',
  fontSize: '32px',
  fontFamily: 'Arial, sans-serif',
  textAlign: 'center',
  margin: '0',
  textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
  fontWeight: 'bold'
};

// Estilos para la tarjeta del formulario
export const formCardStyles = {
  backgroundColor: 'white',
  padding: '40px',
  borderRadius: '12px',
  boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
  width: '350px',
  border: '2px solid #e2e8f0'
};

// Estilos para el contenedor del formulario
export const formContainerStyles = {
  textAlign: 'center'
};

// Estilos para el subtítulo del formulario
export const formSubtitleStyles = {
  marginBottom: '25px',
  color: '#4a5568',
  fontSize: '20px',
  fontWeight: 'bold'
};

// Estilos base para los campos de entrada
export const inputBaseStyles = {
  width: '100%',
  padding: '15px',
  border: '2px solid #e2e8f0',
  borderRadius: '8px',
  fontSize: '16px',
  boxSizing: 'border-box'
};

// Estilos específicos para el campo de usuario
export const usernameInputStyles = {
  ...inputBaseStyles,
  marginBottom: '20px'
};

// Estilos específicos para el campo de contraseña
export const passwordInputStyles = {
  ...inputBaseStyles,
  marginBottom: '25px'
};

// Estilos para el botón principal de login
export const loginButtonStyles = {
  width: '100%',
  padding: '15px',
  backgroundColor: '#3182ce',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  fontSize: '18px',
  fontWeight: 'bold',
  cursor: 'pointer',
  transition: 'background-color 0.3s'
};

// Estilos para el texto de ayuda
export const helpTextStyles = {
  marginTop: '20px',
  fontSize: '14px',
  color: '#718096',
  fontStyle: 'italic'
};

// Estilos para el botón de test
export const testButtonStyles = {
  marginTop: '15px',
  padding: '8px 16px',
  backgroundColor: '#38a169',
  color: 'white',
  border: 'none',
  borderRadius: '6px',
  fontSize: '14px',
  cursor: 'pointer'
};

// Estilos para el loading spinner
export const loadingContainerStyles = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  height: '100vh',
  fontSize: '18px'
};

// Efectos hover para botones (funciones)
export const getHoverEffects = () => ({
  loginButton: {
    onMouseOver: (e) => e.target.style.backgroundColor = '#2c5aa0',
    onMouseOut: (e) => e.target.style.backgroundColor = '#3182ce'
  }
});
