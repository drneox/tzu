import React from "react";
import {
  Box,
  Drawer,
  DrawerBody,
  DrawerContent,
  DrawerHeader,
  DrawerOverlay,
  Flex,
  IconButton,
  VStack,
  useDisclosure,
} from "@chakra-ui/react";
import { HamburgerIcon } from "@chakra-ui/icons";
import { Link, useLocation } from "react-router-dom";
import { useLocalization } from '../hooks/useLocalization';
import { navBarStyle } from '../styles/HeaderStyles';
import { useAuth } from '../context/AuthContext';
import { colors } from '../theme/colors';

const NavLink = ({ to, children, exact, onNavigate, mobile = false }) => {
  const { pathname } = useLocation();
  const isActive = exact ? pathname === to : pathname.startsWith(to);

  return (
    <Link
      to={to}
      style={{
        textDecoration: 'none',
        color: isActive ? colors.nav.activeText : colors.nav.inactiveText,
        fontSize: mobile ? '0.95rem' : '0.78rem',
        fontWeight: isActive ? '700' : '500',
        padding: mobile ? '10px 12px' : '4px 9px',
        borderRadius: mobile ? '10px' : '20px',
        background: isActive ? colors.nav.activeBg : colors.transparent,
        opacity: isActive ? 1 : 0.9,
        transition: 'all 0.15s',
        whiteSpace: mobile ? 'normal' : 'nowrap',
        flex: mobile ? '1 1 auto' : '0 0 auto',
        width: mobile ? '100%' : 'auto',
      }}
      onClick={onNavigate}
      onMouseEnter={(event) => {
        if (!isActive) {
          event.currentTarget.style.opacity = '1';
          event.currentTarget.style.background = colors.nav.hoverBg;
        }
      }}
      onMouseLeave={(event) => {
        if (!isActive) {
          event.currentTarget.style.opacity = '0.9';
          event.currentTarget.style.background = colors.transparent;
        }
      }}
    >
      {children}
    </Link>
  );
};

const Navigation = () => {
  const { t } = useLocalization();
  const { isAdmin, canWrite } = useAuth();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const navItems = [
    { to: '/', label: t?.dashboard?.nav_label || 'Dashboard', exact: true },
    { to: '/create', label: t.ui.menu.new_analysis },
    { to: '/systems', label: t.ui.menu.archive, exact: true },
    ...(canWrite ? [{ to: '/projects', label: t?.projects?.title || 'Proyectos' }] : []),
    { to: '/reports', label: t.ui.menu.reports },
    ...(isAdmin ? [{ to: '/users', label: t.ui.menu.users }] : []),
  ];

  return (
    <>
      <Flex {...navBarStyle} display={{ base: 'none', md: 'flex' }}>
        {navItems.map((item) => (
          <NavLink key={item.to} to={item.to} exact={item.exact}>
            {item.label}
          </NavLink>
        ))}
      </Flex>

      <Box display={{ base: 'block', md: 'none' }}>
        <IconButton
          aria-label="Abrir navegación"
          icon={<HamburgerIcon />}
          variant="outline"
          size="sm"
          onClick={onOpen}
        />
      </Box>

      <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerHeader borderBottomWidth="1px">Menú</DrawerHeader>
          <DrawerBody>
            <VStack align="stretch" spacing={2} mt={2}>
              {navItems.map((item) => (
                <NavLink
                  key={`mobile-${item.to}`}
                  to={item.to}
                  exact={item.exact}
                  onNavigate={onClose}
                  mobile
                >
                  {item.label}
                </NavLink>
              ))}
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
};

export default Navigation;
