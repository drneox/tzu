/**
 * Componente Principal de la Aplicación
 * Archivo: App.js
 * Propósito: Punto de entrada principal con sistema de autenticación
 * 
 * Características:
 * - Sistema de login con JWT y localStorage
 * - Routing condicional basado en autenticación
 * - Componentes separados para login, loading y app principal
 * - Gestión centralizada del estado de autenticación con Context API
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ChakraProvider } from '@chakra-ui/react';
import './App.css';

// Context de autenticación
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

// Componentes de autenticación
import Login from './components/Login';
import LoadingScreen from './components/LoadingScreen';

// Componentes principales de la aplicación
import Header from './components/Header';
import Footer from './components/Footer';
import Index from './components/Index';
import List from './components/List';
import Analysis from './components/Analysis';
import CreateInformationSystem from './components/CreateInformationSystem';
import UploadDiagram from './components/UploadDiagram';

// Componente AppContent - Contenido principal de la aplicación
function AppContent() {
  const { isAuthenticated, logout, isLoading } = useAuth();

  // Manejador para cerrar sesión
  const handleLogout = () => {
    logout();
  };

  // Si está cargando, mostrar pantalla de carga
  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <div className="App">
      {/* Header con función de logout solo si está autenticado */}
      {isAuthenticated && <Header onLogout={handleLogout} />}
      
      {/* Contenido principal con routing */}
      <main>
        <Routes>
          {/* Ruta de login - accesible solo cuando NO está autenticado */}
          <Route 
            path="/login" 
            element={
              isAuthenticated 
                ? <Navigate to="/" replace /> 
                : <Login onLogin={(status) => {}} />
            } 
          />
          
          {/* Rutas protegidas - requieren autenticación */}
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <Index />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/list" 
            element={
              <ProtectedRoute>
                <List />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/analysis" 
            element={
              <ProtectedRoute>
                <Analysis />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/analysis/:id" 
            element={
              <ProtectedRoute>
                <Analysis />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/create" 
            element={
              <ProtectedRoute>
                <CreateInformationSystem />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/upload/:id" 
            element={
              <ProtectedRoute>
                <UploadDiagram />
              </ProtectedRoute>
            } 
          />
          
          {/* Redirección por defecto */}
          <Route path="*" element={
            isAuthenticated 
              ? <Navigate to="/" replace /> 
              : <Navigate to="/login" replace />
          } />
        </Routes>
      </main>
      
      {/* Footer solo si está autenticado */}
      {isAuthenticated && <Footer />}
    </div>
  );
}

/**
 * Componente App Principal
 * Configura el proveedor de autenticación y el tema de Chakra UI
 */
function App() {
  return (
    <ChakraProvider>
      <AuthProvider>
        <Router>
          <AppContent />
        </Router>
      </AuthProvider>
    </ChakraProvider>
  );
}

export default App;
