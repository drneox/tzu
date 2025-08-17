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
export const getInformationSystems = async (skip = 0, limit = 10) => {
  try {
    // Primero obtenemos el total de sistemas (sin límite)
    const countResponse = await apiClient.get(`/information_systems?skip=0&limit=1000`);
    const totalCount = countResponse.data.length;
    
    // Luego obtenemos los datos paginados
    const dataResponse = await apiClient.get(`/information_systems?skip=${skip}&limit=${limit}`);
    
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
 * Sube y procesa un diagrama para un sistema de información
 * @param {string} id - ID del sistema
 * @param {File} file - Archivo de imagen del diagrama
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
 * Acceso directo para obtener los datos completos de un sistema por su ID
 * @param {string} id - ID del sistema
 * @returns {Promise} - Promise con los datos del sistema
 */
export const fetchInformationSystemById = async (id) => {
  const res = await getInformationSystemById(id);
  return res.data;
};
