import React, { createContext, useState, useEffect, useContext } from 'react';
import { getCurrentUser } from '../services';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshSession = async () => {
    try {
      const userData = await getCurrentUser();
      setUser(userData);
      setIsAuthenticated(true);
      return userData;
    } catch {
      setIsAuthenticated(false);
      setUser(null);
      return null;
    }
  };

  useEffect(() => {
    const checkAuth = async () => {
      await refreshSession();
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async () => {
    await refreshSession();
  };

  const logout = () => {
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
    isLoading,
    role: user?.role ?? null,
    isAdmin: user?.role === 'admin',
    canWrite: ['admin', 'analyst'].includes(user?.role)
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
