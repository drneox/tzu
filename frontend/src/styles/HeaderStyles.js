// Contenedor principal del header — una sola fila horizontal
export const headerContainer = {
  as: "header",
  align: "center",
  px: "1.25rem",
  h: "56px",
  bg: "#00243c",
  color: "#ffa833",
  boxShadow: "0 1px 0 rgba(255,168,51,0.15)"
};

// Fila única que distribuye logo | nav | controles
export const contentContainer = {
  direction: "row",
  align: "center",
  justify: "space-between",
  width: "100%",
  gap: 6
};

// Bloque logo + nombre
export const topRowContainer = {
  alignItems: "center",
  gap: "10px",
  flexShrink: 0
};

// Barra de nav links
export const navBarStyle = {
  as: "nav",
  align: "center",
  gap: 1,
  flex: 1
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

// navLinkStyle ya no se usa directamente (Navigation usa estilos inline con estado activo)
export const navLinkStyle = {
  textDecoration: 'none',
  color: '#ffa833'
};
