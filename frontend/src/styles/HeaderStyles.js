/**
 * Estilos para el componente Header
 * 
 * Este archivo contiene todos los estilos utilizados en el componente Header,
 * siguiendo las buenas prácticas de separación de concerns en React.
 */

// Estilo para el contenedor principal del encabezado
export const headerContainer = {
  as: "nav",
  align: "center",
  wrap: "wrap",
  padding: "0.5rem",
  bg: "#00243c",
  color: "#ffa833"
};

// Estilo para el contenedor de contenido del encabezado
export const contentContainer = {
  direction: "column", 
  align: "left", 
  width: "100%"
};

// Estilo para la fila superior que contiene el logo y el área de usuario
export const topRowContainer = {
  alignItems: "center", 
  justifyContent: "space-between", 
  width: "100%"
};

// Estilo para el botón del menú de usuario
export const userMenuButtonStyle = {
  variant: "ghost",
  color: "#ffa833",
  _hover: { bg: "rgba(255, 168, 51, 0.1)" },
  _active: { bg: "rgba(255, 168, 51, 0.2)" },
  fontSize: "sm"
};

// Estilo para los elementos del menú de usuario
export const userMenuItemStyle = {
  color: "gray.700",
  _hover: { bg: "gray.100" }
};

// Estilo para el elemento de cerrar sesión
export const logoutMenuItemStyle = {
  color: "red.500",
  _hover: { bg: "red.50" }
};

// Estilo para la barra de navegación inferior
export const navBarStyle = {
  width: "300px",
  justifyContent: "space-between",
  mt: 4
};

// Estilo para los enlaces de navegación
export const navLinkStyle = {
  textDecoration: 'none', 
  color: '#ffa833'
};
