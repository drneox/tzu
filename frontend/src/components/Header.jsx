import React from "react";
import { 
  Heading, 
  Flex, 
  HStack, 
  Box
} from "@chakra-ui/react";
import LanguageSwitcher from './LanguageSwitcher';
import { useLocalization } from '../hooks/useLocalization';
import Logo from './Logo';
import UserMenu from './UserMenu';
import Navigation from './Navigation';

// Importar estilos
import {
  headerContainer,
  contentContainer,
  topRowContainer
} from '../styles/HeaderStyles';

const Header = ({ onLogout }) => {
  const { t } = useLocalization();

  return (
    <Flex {...headerContainer}>
      <Flex {...contentContainer}>
        <Flex {...topRowContainer}>
          <Heading as="h1" size="xl" display="flex" flexDirection="row" textAlign="center" alignItems="center" >
            <Logo />
            <Box ml={2}>
              <h1>Threat Zero Utility</h1>
            </Box>
          </Heading>
          
          {/* Área derecha con idioma y usuario */}
          <HStack spacing={4}>
            <LanguageSwitcher />
            <UserMenu />
          </HStack>
        </Flex>
        
        <Navigation />
      </Flex>
    </Flex>
  );
};

export default Header;