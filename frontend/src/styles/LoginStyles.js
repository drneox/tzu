/**
 * Estilos centralizados para el sistema de login
 * Archivo: LoginStyles.js
 * Propósito: Contener todos los estilos del login en un lugar centralizado
 *
 * Nota: el login principal usa Login.jsx con Chakra UI. Este archivo se mantiene
 * para compatibilidad con LoginForm.jsx y cualquier otra referencia legacy.
 */

import { colors } from '../theme/colors';

// Estilos para el contenedor principal del login
export const loginContainerStyles = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
  background: colors.login.bg,
  flexDirection: 'column',
  gap: '30px'
};

// Estilos para el logo TZU
export const logoStyles = {
  width: '120px',
  height: 'auto',
  backgroundColor: 'transparent',
  borderRadius: '50%',
  padding: '10px',
  border: `2px solid ${colors.primary.default}`,
};

// Estilos para el título principal
export const mainTitleStyles = {
  color: colors.login.title,
  fontSize: '28px',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  textAlign: 'center',
  margin: '0',
  fontWeight: 'bold'
};

// Estilos para la tarjeta del formulario
export const formCardStyles = {
  backgroundColor: colors.login.cardBg,
  padding: '40px',
  borderRadius: '12px',
  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
  width: '350px',
  border: `1px solid ${colors.login.inputBorder}`
};

// Estilos para el contenedor del formulario
export const formContainerStyles = {
  textAlign: 'center'
};

// Estilos para el subtítulo del formulario
export const formSubtitleStyles = {
  marginBottom: '25px',
  color: colors.login.subtitle,
  fontSize: '20px',
  fontWeight: 'bold'
};

// Estilos base para los campos de entrada
export const inputBaseStyles = {
  width: '100%',
  padding: '15px',
  border: `2px solid ${colors.login.inputBorder}`,
  borderRadius: '8px',
  fontSize: '16px',
  boxSizing: 'border-box',
  backgroundColor: colors.login.inputBg
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
  backgroundColor: colors.primary.default,
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  fontSize: '18px',
  fontWeight: 'bold',
  cursor: 'pointer',
  transition: 'background-color 0.2s, transform 0.2s'
};

// Estilos para el texto de ayuda
export const helpTextStyles = {
  marginTop: '20px',
  fontSize: '14px',
  color: colors.text.secondary,
  fontStyle: 'italic'
};

// Estilos para el botón de test
export const testButtonStyles = {
  marginTop: '15px',
  padding: '8px 16px',
  backgroundColor: colors.text.muted,
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
  fontSize: '18px',
  color: colors.text.secondary,
  backgroundColor: colors.background
};

// Efectos hover para botones (funciones)
export const getHoverEffects = () => ({
  loginButton: {
    onMouseOver: (e) => {
      e.target.style.backgroundColor = colors.primary.hover;
      e.target.style.transform = 'translateY(-1px)';
    },
    onMouseOut: (e) => {
      e.target.style.backgroundColor = colors.primary.default;
      e.target.style.transform = 'translateY(0)';
    }
  }
});
