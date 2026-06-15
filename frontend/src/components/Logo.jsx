import React from "react";
import { Box } from "@chakra-ui/react";

/**
 * Componente Logo
 * Renderiza el logo de la aplicación TZU
 *
 * Dimensiones basadas en el diseño del SaaS:
 * - size: 64px
 * - cropScale: 1.45 (zoom para recortar espacio sobrante del arte)
 */
const Logo = ({ size = '64px', cropScale = 1.45, p = '0px' }) => {
  return (
    <Box
      className="logo-container"
      boxSize={size}
      overflow="hidden"
      display="flex"
      alignItems="center"
      justifyContent="center"
      flexShrink={0}
      p={p}
    >
      <img
        className="header_image"
        src="/logo.png"
        alt="TZU Security Logo"
        style={{
          width: "100%",
          height: "100%",
          display: "block",
          objectFit: "contain",
          transform: `scale(${cropScale})`,
          transformOrigin: "center",
        }}
        onError={(e) => { e.currentTarget.src = "/tzu.png"; }}
      />
    </Box>
  );
};

export default Logo;
