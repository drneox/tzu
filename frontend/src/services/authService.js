/**
 * Servicios de autenticación
 * Gestiona operaciones relacionadas con usuarios: login, registro, etc.
 */
import apiClient, { API_BASE_URL } from './apiClient';
import axios from 'axios'; // Importamos axios directamente para el caso especial del login

/**
 * Inicia sesión de usuario
 * @param {Object} loginData - Datos de inicio de sesión {username, password}
 * @returns {Promise} - Promise con datos de autenticación
 */
export const loginUser = async (loginData) => {
  try {
    // La API de FastAPI espera los datos en formato 'application/x-www-form-urlencoded' para OAuth
    const formData = new URLSearchParams();
    formData.append('username', loginData.username);
    formData.append('password', loginData.password);

    // Usamos axios directamente para este caso especial ya que necesitamos un Content-Type diferente
    const response = await axios.post(`${API_BASE_URL}/token`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Error en inicio de sesión:', error);
    throw new Error(error.response?.data?.detail || 'Error al iniciar sesión');
  }
};

/**
 * Registra un nuevo usuario
 * @param {Object} userData - Datos del usuario a registrar
 * @returns {Promise} - Promise con los datos del usuario registrado
 */
export const registerUser = async (userData) => {
  try {
    const response = await apiClient.post('/users/', userData);
    return response.data;
  } catch (error) {
    console.error('Error en registro:', error);
    throw new Error(error.response?.data?.detail || 'Error al registrar usuario');
  }
};

/**
 * Obtiene información del usuario actualmente autenticado
 * @returns {Promise} - Promise con los datos del usuario
 */
export const getCurrentUser = async () => {
  try {
    const response = await apiClient.get('/users/me');
    return response.data;
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener datos del usuario');
  }
};
