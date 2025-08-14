import React, { createContext, useState, useEffect, useContext } from 'react';
import { getCurrentUser } from '../services';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      const storedAuth = localStorage.getItem('isAuthenticated');
      
      if (token && storedAuth === 'true') {
        try {
          const userData = await getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (error) {
          console.error('Error al verificar autenticación:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('isAuthenticated');
          setIsAuthenticated(false);
        }
      } else {
        setIsAuthenticated(false);
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = (token, userName) => {
    localStorage.setItem('token', token);
    localStorage.setItem('isAuthenticated', 'true');
    setIsAuthenticated(true);
    
    // También intentamos obtener los datos del usuario
    try {
      getCurrentUser().then(userData => {
        console.log("Datos de usuario recibidos:", userData);
        setUser(userData);
      }).catch(error => {
        console.error('Error al obtener datos de usuario después del login:', error);
      });
    } catch (error) {
      console.error('Error al obtener datos de usuario:', error);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('isAuthenticated');
    setIsAuthenticated(false);
    setUser(null);
  };

  const value = {
    isAuthenticated,
    setIsAuthenticated,
    user,
    setUser,
    login,
    logout,
    isLoading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
