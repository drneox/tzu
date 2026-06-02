import React from "react";
import { Flex } from "@chakra-ui/react";
import { Link, useLocation } from "react-router-dom";
import { useLocalization } from '../hooks/useLocalization';
import { navBarStyle } from '../styles/HeaderStyles';
import { useAuth } from '../context/AuthContext';

const NavLink = ({ to, children, exact }) => {
  const { pathname } = useLocation();
  const isActive = exact ? pathname === to : pathname.startsWith(to);

  return (
    <Link
      to={to}
      style={{
        textDecoration: 'none',
        color: isActive ? '#00243c' : '#ffa833',
        fontSize: '0.8rem',
        fontWeight: isActive ? '700' : '500',
        padding: '4px 9px',
        borderRadius: '20px',
        background: isActive ? '#ffa833' : 'transparent',
        opacity: isActive ? 1 : 0.75,
        transition: 'all 0.15s',
        whiteSpace: 'nowrap',
      }}
      onMouseEnter={e => { if (!isActive) { e.currentTarget.style.opacity = 1; e.currentTarget.style.background = 'rgba(255,168,51,0.12)'; } }}
      onMouseLeave={e => { if (!isActive) { e.currentTarget.style.opacity = 0.75; e.currentTarget.style.background = 'transparent'; } }}
    >
      {children}
    </Link>
  );
};

const Navigation = () => {
  const { t } = useLocalization();
  const { isAdmin, canWrite } = useAuth();

  return (
    <Flex {...navBarStyle}>
      <NavLink to="/" exact>{t?.dashboard?.nav_label || 'Dashboard'}</NavLink>
      <NavLink to="/create">{t.ui.menu.new_analysis}</NavLink>
      <NavLink to="/systems" exact>{t.ui.menu.archive}</NavLink>
      {canWrite && <NavLink to="/projects">{t?.projects?.title || 'Proyectos'}</NavLink>}
      <NavLink to="/reports">{t.ui.menu.reports}</NavLink>
      {isAdmin && <NavLink to="/users">{t.ui.menu.users}</NavLink>}
    </Flex>
  );
};

export default Navigation;
