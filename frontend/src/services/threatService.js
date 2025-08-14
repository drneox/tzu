/**
 * Servicios para Amenazas
 * Gestiona operaciones relacionadas con amenazas: CRUD, evaluación de riesgo, etc.
 */
import apiClient from './apiClient';

/**
 * Actualiza el riesgo de múltiples amenazas en un lote
 * @param {string} systemId - ID del sistema
 * @param {Array} updates - Lista de actualizaciones de riesgo
 * @returns {Promise} - Promise con la respuesta del servidor
 */
export const updateThreatsRiskBatch = async (systemId, updates) => {
  try {
    return await apiClient.put(`/information_systems/${systemId}/threats/risk/batch`, updates);
  } catch (error) {
    console.error('Error al actualizar riesgos en lote:', error);
    throw new Error(error.response?.data?.detail || 'Error al actualizar riesgos');
  }
};

/**
 * Actualiza el riesgo residual de una amenaza
 * @param {string} threatId - ID de la amenaza
 * @param {number} residualRiskValue - Valor del riesgo residual (1-9)
 * @returns {Promise} - Promise con los datos de la amenaza actualizada
 */
export const updateThreatResidualRisk = async (threatId, residualRiskValue) => {
  try {
    return await apiClient.put(`/threat/${threatId}/residual-risk`, { residual_risk: residualRiskValue });
  } catch (error) {
    console.error('Error al actualizar riesgo residual:', error);
    throw new Error(error.response?.data?.detail || 'Error al actualizar riesgo residual');
  }
};

/**
 * Actualiza el riesgo residual de múltiples amenazas en un lote
 * @param {string} systemId - ID del sistema
 * @param {Array} updates - Lista de actualizaciones de riesgo residual
 * @returns {Promise} - Promise con la respuesta del servidor
 */
export const updateThreatsResidualRiskBatch = async (systemId, updates) => {
  try {
    return await apiClient.put(`/information_systems/${systemId}/threats/residual-risk/batch`, updates);
  } catch (error) {
    console.error('Error al actualizar riesgos residuales en lote:', error);
    throw new Error(error.response?.data?.detail || 'Error al actualizar riesgos residuales');
  }
};

/**
 * Crea una nueva amenaza para un sistema
 * @param {string} systemId - ID del sistema
 * @param {Object} threatData - Datos de la amenaza a crear
 * @returns {Promise} - Promise con los datos de la amenaza creada
 */
export const createThreatForSystem = async (systemId, threatData) => {
  try {
    return await apiClient.post(`/information_systems/${systemId}/threats`, threatData);
  } catch (error) {
    console.error('Error al crear amenaza:', error);
    throw new Error(error.response?.data?.detail || 'Error al crear amenaza');
  }
};
