import React from "react";
import { Flex, HStack, Text, Box } from "@chakra-ui/react";
import LanguageSwitcher from './LanguageSwitcher';
import Logo from './Logo';
import UserMenu from './UserMenu';
import Navigation from './Navigation';

import {
  headerContainer,
  contentContainer,
  topRowContainer
} from '../styles/HeaderStyles';

const Header = ({ onLogout }) => {
  return (
    <Flex {...headerContainer}>
      <Flex {...contentContainer}>
        {/* Logo + nombre */}
        <HStack {...topRowContainer}>
          <Logo />
          <Text fontWeight="bold" fontSize="md" color="#ffa833" whiteSpace="nowrap">
            Threat Zero Utility
          </Text>
        </HStack>

        {/* Links de navegación */}
        <Navigation />

        {/* Idioma y usuario */}
        <HStack spacing={3} flexShrink={0}>
          <LanguageSwitcher />
          <UserMenu />
        </HStack>
      </Flex>
    </Flex>
  );
};

export default Header;