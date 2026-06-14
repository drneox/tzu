/**
 * Cliente API centralizado
 * Configuración y gestión de solicitudes HTTP para toda la aplicación
 */
import axios from 'axios';

// URL base para todas las peticiones a la API
export const API_BASE_URL = 'http://localhost:3434/api';

// Instancia de axios con configuración común
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

// ========================================
// USER MANAGEMENT FUNCTIONS
// ========================================

export const getUsers = async (params = {}) => {
  const response = await apiClient.get('/users', { params });
  return response.data;
};

export const createUser = async (userData) => {
  const response = await apiClient.post('/users', userData);
  return response.data;
};

export const updateUserRole = async (userId, role) => {
  const response = await apiClient.put(`/users/${userId}/role`, { role });
  return response.data;
};

export const updateUserActive = async (userId, isActive) => {
  const response = await apiClient.put(`/users/${userId}/active`, { is_active: isActive });
  return response.data;
};

export const deleteUser = async (userId) => {
  const response = await apiClient.delete(`/users/${userId}`);
  return response.data;
};

export const getAuditLog = async (params = {}) => {
  const response = await apiClient.get('/admin/audit-log', { params });
  return response.data;
};

// ========================================
// DASHBOARD FUNCTIONS
// ========================================

export const getDashboardStats = async (projectId = null) => {
  const params = {};
  if (projectId) params.project_id = projectId;
  const response = await apiClient.get('/dashboard/stats', { params });
  return response.data;
};
