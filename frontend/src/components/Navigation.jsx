import React from "react";
import { Flex } from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { useLocalization } from '../hooks/useLocalization';
import { navBarStyle, navLinkStyle } from '../styles/HeaderStyles';

/**
 * Componente Navigation
 * Barra de navegación principal de la aplicación
 */
const Navigation = () => {
  const { t } = useLocalization();

  return (
    <Flex {...navBarStyle}>
      <Link to="/create" style={navLinkStyle}>
        <h3>{t.ui.menu.new_analysis}</h3>
      </Link>
      <Link to="/" style={navLinkStyle}>
        <h3>{t.ui.menu.archive}</h3>
      </Link>
    </Flex>
  );
};

export default Navigation;
