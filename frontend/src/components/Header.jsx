import React from "react";
import { Flex, HStack, Text } from "@chakra-ui/react";
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
          <Text fontWeight="bold" fontSize="md" color="indigo.700" whiteSpace="nowrap">
            TZU
          </Text>
        </HStack>

        {/* Links de navegación */}
        <Navigation />

        {/* Idioma y usuario */}
        <HStack
          spacing={3}
          flexShrink={0}
          ml={{ base: "auto", md: 0 }}
          order={{ base: 2, md: 0 }}
        >
          <LanguageSwitcher />
          <UserMenu />
        </HStack>
      </Flex>
    </Flex>
  );
};

export default Header;
