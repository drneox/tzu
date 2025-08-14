/**
 * Cliente API centralizado
 * Configuración y gestión de solicitudes HTTP para toda la aplicación
 */
import axios from 'axios';

// URL base para todas las peticiones a la API
export const API_BASE_URL = 'http://localhost:8000';

// Instancia de axios con configuración común
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir el token de autenticación a las peticiones
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar errores de respuesta
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Manejar errores comunes como 401, 403, etc.
    if (error.response && error.response.status === 401) {
      // Redireccionar al login o limpiar sesión
      localStorage.removeItem('token');
      localStorage.removeItem('isAuthenticated');
    }
    return Promise.reject(error);
  }
);

export default apiClient;
