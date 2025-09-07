/**
 * Servicios API Centralizados
 * Archivo index que exporta todos los servicios disponibles en la aplicación
 */

// Importar todos los servicios
import apiClient, { API_BASE_URL } from './apiClient';
import * as authService from './authService';
import * as informationSystemService from './informationSystemService';
import * as threatService from './threatService';

// Exportar todos los servicios
export const { 
  loginUser,
  registerUser,
  getCurrentUser
} = authService;

export const {
  getInformationSystems,
  getInformationSystemById,
  createInformationSystem,
  uploadDiagram,
  fetchInformationSystemById
} = informationSystemService;

export const {
  getThreatsReport,
  getAllThreats,
  updateThreatsRiskBatch,
  createThreatForSystem,
  updateThreatResidualRisk,
  updateThreatsResidualRiskBatch,
  updateThreatRisk,
  deleteThreat
} = threatService;

// Para mantener compatibilidad con código antiguo
export const getInformationSystemsById = informationSystemService.getInformationSystemById;

// También exportamos el cliente API y la URL base por si algún componente necesita acceso directo
export { apiClient, API_BASE_URL };

// ========================================
// SERVICIOS DE CONTROL TAGS
// ========================================

/**
 * Obtiene sugerencias de tags de control basadas en categoría STRIDE
 */
export const fetchControlTagSuggestions = async (strideCategory) => {
  try {
    // Add cache buster to ensure we get fresh data
    const cacheBuster = Date.now();
    const response = await apiClient.get(`/control-tags/suggestions/${strideCategory}?t=${cacheBuster}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching control tag suggestions:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener sugerencias de tags');
  }
};

/**
 * Busca tags de control existentes
 */
export const searchControlTags = async (query) => {
  try {
    const response = await apiClient.get(`/control-tags/search?query=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    console.error('Error searching control tags:', error);
    throw new Error(error.response?.data?.detail || 'Error al buscar tags');
  }
};

/**
 * Valida el formato de un tag de control
 */
export const validateControlTag = async (tag) => {
  try {
    const response = await apiClient.get(`/control-tags/validate/${encodeURIComponent(tag)}`);
    return response.data;
  } catch (error) {
    console.error('Error validating control tag:', error);
    throw new Error(error.response?.data?.detail || 'Error al validar tag');
  }
};

/**
 * Actualiza los tags de control de una remediación
 */
export const updateRemediationTags = async (threatId, controlTags) => {
  try {
    const response = await apiClient.put(`/threats/${threatId}/remediation/tags`, {
      control_tags: controlTags
    });
    return response.data;
  } catch (error) {
    console.error('Error updating remediation tags:', error);
    throw new Error(error.response?.data?.detail || 'Error al actualizar tags de remediación');
  }
};

/**
 * Obtiene todos los estándares disponibles
 */
export const fetchAvailableStandards = async () => {
  try {
    const response = await apiClient.get('/control-tags/standards');
    return response.data;
  } catch (error) {
    console.error('Error fetching available standards:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener estándares disponibles');
  }
};

/**
 * Obtiene la jerarquía completa de control tags
 */
export const fetchControlTagsHierarchy = async () => {
  try {
    const response = await apiClient.get('/control-tags/hierarchy');
    return response.data;
  } catch (error) {
    console.error('Error fetching control tags hierarchy:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener jerarquía de control tags');
  }
};

/**
 * Obtiene control tags por estándar específico
 */
export const fetchControlTagsByStandard = async (standard) => {
  try {
    const response = await apiClient.get(`/control-tags/by-standard/${standard}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching control tags by standard:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener control tags por estándar');
  }
};

/**
 * Obtiene control tags por estándar y categoría STRIDE
 */
export const fetchControlTagsByStandardAndCategory = async (standard, strideCategory) => {
  try {
    const response = await apiClient.get(`/control-tags/by-standard/${standard}/category/${encodeURIComponent(strideCategory)}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching control tags by standard and category:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener control tags por estándar y categoría');
  }
};

/**
 * Categoriza una lista de tags por estándar
 */
export const categorizeControlTags = async (tags) => {
  try {
    const response = await apiClient.post('/control-tags/categorize', tags);
    return response.data;
  } catch (error) {
    console.error('Error categorizing control tags:', error);
    throw new Error(error.response?.data?.detail || 'Error al categorizar control tags');
  }
};

