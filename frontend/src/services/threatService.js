/**
 * Servicios para Amenazas
 * Gestiona operaciones relacionadas con amenazas: CRUD, evaluación de riesgo, etc.
 */
import apiClient from './apiClient';

/**
 * Obtiene un reporte de amenazas con filtros opcionales
 * @param {Object} params - Parámetros de consulta
 * @param {number} params.skip - Número de registros a omitir
 * @param {number} params.limit - Límite de registros a obtener
 * @param {Array} params.standards - Lista de estándares para filtrar
 * @param {string} params.systemId - ID del sistema de información
 * @param {string} params.riskLevel - Nivel de riesgo a filtrar (deprecated, usar inherit_risk o current_risk)
 * @param {string} params.inherit_risk - Filtro por riesgo inherente (LOW, MEDIUM, HIGH, CRITICAL)
 * @param {string} params.current_risk - Filtro por riesgo actual (LOW, MEDIUM, HIGH, CRITICAL)
 * @returns {Promise} - Promise con el reporte de amenazas filtradas
 */
export const getThreatsReport = async ({ 
  skip = 0, 
  limit = 1000, 
  standards = null, 
  systemId = null, 
  riskLevel = null,
  inherit_risk = null,
  current_risk = null
} = {}) => {
  try {
    const params = { skip, limit };
    
    // Agregar parámetros de filtrado si están presentes
    if (standards && standards.length > 0) {
      params.standards = standards.join(',');
    }
    if (systemId) {
      params.system_id = systemId;
    }
    if (riskLevel) {
      params.risk_level = riskLevel;
    }
    if (inherit_risk) {
      params.inherit_risk = inherit_risk;
    }
    if (current_risk) {
      params.current_risk = current_risk;
    }
    
    const response = await apiClient.get('/report', { params });
    return response.data;
  } catch (error) {
    console.error('Error al obtener reporte de amenazas:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener reporte de amenazas');
  }
};

// Alias para compatibilidad con código existente
export const getAllThreats = getThreatsReport;

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

/**
 * Actualiza los factores de riesgo OWASP de una amenaza
 * @param {string} threatId - ID de la amenaza
 * @param {Object} riskData - Datos de riesgo OWASP
 * @returns {Promise} - Promise con los datos de la amenaza actualizada
 */
export const updateThreatRisk = async (threatId, riskData) => {
  try {
    return await apiClient.put(`/threat/${threatId}/risk`, riskData);
  } catch (error) {
    console.error('Error al actualizar riesgo de amenaza:', error);
    throw new Error(error.response?.data?.detail || 'Error al actualizar riesgo');
  }
};

/**
 * Elimina una amenaza
 * @param {string} threatId - ID de la amenaza a eliminar
 * @returns {Promise} - Promise con la confirmación de eliminación
 */
export const deleteThreat = async (threatId) => {
  try {
    return await apiClient.delete(`/threat/${threatId}`);
  } catch (error) {
    console.error('Error al eliminar amenaza:', error);
    throw new Error(error.response?.data?.detail || 'Error al eliminar amenaza');
  }
};
