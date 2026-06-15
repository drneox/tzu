import { colors } from '../theme/colors';

// Contenedor principal del header — look limpio y minimalista
export const headerContainer = {
  as: "header",
  align: "center",
  px: "1rem",
  minH: { base: "56px", md: "64px" },
  py: { base: 2, md: 0 },
  bg: colors.header.bg,
  color: colors.header.text,
  boxShadow: "sm",
  borderBottom: "1px solid",
  borderColor: colors.header.border,
  position: "sticky",
  top: 0,
  zIndex: 1000,
};

// Fila única que distribuye logo | nav | controles
export const contentContainer = {
  direction: "row",
  align: { base: "center", md: "center" },
  justify: "space-between",
  flexWrap: { base: "wrap", md: "nowrap" },
  width: "100%",
  gap: { base: 2, md: 3 },
  maxW: "1400px",
  mx: "auto",
};

// Bloque logo + nombre
export const topRowContainer = {
  alignItems: "center",
  gap: "10px",
  flexShrink: 0,
};

// Barra de nav links
export const navBarStyle = {
  as: "nav",
  align: "center",
  gap: 2,
  flex: 1,
  justify: "center",
};

// Estilo para el botón del menú de usuario
export const userMenuButtonStyle = {
  variant: "outline",
  color: colors.header.text,
  bg: colors.header.bg,
  borderColor: colors.border,
  _hover: { bg: colors.background, borderColor: colors.primary.subtle },
  _active: { bg: colors.primary.light },
  fontSize: "sm",
  fontWeight: "medium",
};

// Estilo para los elementos del menú de usuario
export const userMenuItemStyle = {
  color: colors.text.primary,
  _hover: { bg: colors.background },
};

// Estilo para el elemento de cerrar sesión
export const logoutMenuItemStyle = {
  color: colors.error,
  _hover: { bg: "red.50" },
};

// navLinkStyle ya no se usa directamente (Navigation usa estilos inline con estado activo)
export const navLinkStyle = {
  textDecoration: 'none',
  color: colors.header.text,
};
