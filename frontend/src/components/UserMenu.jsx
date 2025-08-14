import React from "react";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  Button,
  Text,
  Box,
  useToast
} from "@chakra-ui/react";
import { FaUser, FaSignOutAlt, FaChevronDown } from "react-icons/fa";
import { useAuth } from '../context/AuthContext';
import {
  userMenuButtonStyle,
  userMenuItemStyle,
  logoutMenuItemStyle
} from '../styles/HeaderStyles';

/**
 * Componente UserMenu
 * Menú desplegable para el usuario con opciones de perfil y cierre de sesión
 */
const UserMenu = () => {
  const { user, logout } = useAuth();
  const toast = useToast();
  const name = user?.name || 'Usuario';

  const handleLogout = () => {
    logout();
    toast({
      title: "Sesión cerrada",
      description: "Has cerrado sesión correctamente",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Menu>
      <MenuButton
        as={Button}
        rightIcon={<FaChevronDown />}
        leftIcon={<FaUser />}
        {...userMenuButtonStyle}
      >
        {name}
      </MenuButton>
      <MenuList bg="white" borderColor="gray.200">
        <MenuItem 
          icon={<FaUser />}
          {...userMenuItemStyle}
          isDisabled
        >
          <Box>
            <Text fontSize="sm" fontWeight="bold">{name}</Text>
            <Text fontSize="xs" color="gray.500">Conectado</Text>
          </Box>
        </MenuItem>
        <MenuDivider />
        <MenuItem 
          icon={<FaSignOutAlt />}
          {...logoutMenuItemStyle}
          onClick={handleLogout}
        >
          Cerrar Sesión
        </MenuItem>
      </MenuList>
    </Menu>
  );
};

export default UserMenu;
