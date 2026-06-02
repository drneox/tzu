/**
 * Servicios para Sistemas de Información
 * Gestiona operaciones relacionadas con sistemas: CRUD, búsqueda, etc.
 */
import apiClient from './apiClient';

/**
 * Obtiene lista paginada de sistemas de información
 * @param {number} skip - Número de sistemas a saltar para la paginación
 * @param {number} limit - Cantidad máxima de sistemas a recuperar
 * @returns {Promise} - Promise con los datos de sistemas y conteo total
 */
export const getInformationSystems = async (skip = 0, limit = 10, project_id = null, include_archived = false) => {
  try {
    const projectParam = project_id ? `&project_id=${project_id}` : '';
    const archivedParam = include_archived ? '&include_archived=true' : '';
    // Primero obtenemos el total de sistemas (sin límite)
    const countResponse = await apiClient.get(`/information_systems?skip=0&limit=1000${projectParam}${archivedParam}`);
    const totalCount = countResponse.data.length;
    
    // Luego obtenemos los datos paginados
    const dataResponse = await apiClient.get(`/information_systems?skip=${skip}&limit=${limit}${projectParam}${archivedParam}`);
    
    // Agregamos el conteo total a la respuesta
    dataResponse.totalCount = totalCount;
    
    return dataResponse;
  } catch (error) {
    console.error('Error al obtener sistemas de información:', error);
    throw new Error(error.response?.data?.detail || 'Error al obtener sistemas');
  }
};

/**
 * Obtiene un sistema de información por su ID
 * @param {string} id - ID del sistema a recuperar
 * @returns {Promise} - Promise con los datos del sistema
 */
export const getInformationSystemById = async (id) => {
  try {
    return await apiClient.get(`/information_systems/${id}`);
  } catch (error) {
    console.error(`Error al obtener sistema de información (ID: ${id}):`, error);
    throw new Error(error.response?.data?.detail || 'Error al obtener sistema');
  }
};

/**
 * Crea un nuevo sistema de información
 * @param {Object} data - Datos del sistema a crear
 * @returns {Promise} - Promise con los datos del sistema creado
 */
export const createInformationSystem = async (data) => {
  try {
    return await apiClient.post("/new", data);
  } catch (error) {
    console.error('Error al crear sistema de información:', error);
    throw new Error(error.response?.data?.detail || 'Error al crear sistema');
  }
};

/**
 * Sube y procesa un archivo de diagrama para un sistema de información.
 * Soporta imágenes (PNG, JPG, WebP, GIF, BMP), PDF, XML, JSON, SVG, TXT y MD.
 * @param {string} id - ID del sistema
 * @param {File} file - Archivo del diagrama
 * @returns {Promise} - Promise con la respuesta del servidor
 */
export const uploadDiagram = async (id, file) => {
  try {
    console.log(`Preparando para subir archivo ${file.name} para el sistema ${id}`);
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post(`/evaluate/${id}`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    console.log("Respuesta recibida:", response.data);
    return response;
  } catch (error) {
    console.error("Error al subir el diagrama:", error);
    throw error;
  }
};

/**
 * Envía una descripción textual de un sistema para análisis de amenazas.
 * @param {string} id - ID del sistema
 * @param {string} text - Descripción textual de la arquitectura o diagrama
 * @returns {Promise} - Promise con la respuesta del servidor
 */
export const uploadDiagramText = async (id, text) => {
  try {
    console.log(`Enviando descripción de texto para el sistema ${id}`);
    const formData = new FormData();
    formData.append("text_content", text);

    const response = await apiClient.post(`/evaluate/${id}`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    console.log("Respuesta recibida:", response.data);
    return response;
  } catch (error) {
    console.error("Error al enviar descripción de texto:", error);
    throw error;
  }
};

/**
 * Acceso directo para obtener los datos completos de un sistema por su ID
 * @param {string} id - ID del sistema
 * @returns {Promise} - Promise con los datos del sistema
 */
export const fetchInformationSystemById = async (id) => {
  const res = await getInformationSystemById(id);
  return res.data;
};

/**
 * Update an information system (title, description, or project assignment)
 * @param {string} id - Information system UUID
 * @param {object} data - Fields to update: { title, description, project_id }
 * @returns {Promise} - Updated information system
 */
export const updateInformationSystem = async (id, data) => {
  try {
    const response = await apiClient.put(`/information_systems/${id}`, data);
    return response;
  } catch (error) {
    console.error('Error al actualizar sistema de información:', error);
    throw error;
  }
};

/**
 * Toggle archive state of an information system (admin only)
 * @param {string} id - Information system UUID
 * @returns {Promise} - { archived: boolean }
 */
export const archiveInformationSystem = async (id) => {
  try {
    const response = await apiClient.patch(`/information_systems/${id}/archive`);
    return response.data;
  } catch (error) {
    console.error('Error al archivar sistema de información:', error);
    throw error;
  }
};
