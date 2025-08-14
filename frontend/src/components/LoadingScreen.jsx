/**
 * Componente de Loading
 * Archivo: LoadingScreen.jsx
 * Propósito: Pantalla de carga mientras se verifica la autenticación
 * 
 * Características:
 * - Spinner centrado en pantalla
 * - Mensaje de carga
 * - Estilos consistentes con el tema
 */

import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { loadingContainerStyles } from '../styles/LoginStyles';

/**
 * Componente LoadingScreen
 * Muestra un spinner de carga mientras se verifica el estado de autenticación
 */
const LoadingScreen = () => {
  return (
    <ChakraProvider>
      <div style={loadingContainerStyles}>
        {/* Spinner simple con texto */}
        <div>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #3182ce',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }}></div>
          Cargando...
        </div>
        
        {/* CSS para la animación del spinner */}
        <style jsx>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </ChakraProvider>
  );
};

export default LoadingScreen;
