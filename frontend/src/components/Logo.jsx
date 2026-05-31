import React from "react";
import { Box } from "@chakra-ui/react";

/**
 * Componente Logo
 * Renderiza el logo de la aplicación TZU
 */
const Logo = () => {
  return (
    <Box className="logo-container">
      <img 
        className="header_image" 
        src="/tzu.png" 
        alt="TZU Security Logo" 
        style={{ height: "38px", width: "auto", display: "block" }}
      />
    </Box>
  );
};

export default Logo;
