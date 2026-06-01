import apiClient from './apiClient';

export const getProjects = async (skip = 0, limit = 100) => {
  try {
    return await apiClient.get(`/projects?skip=${skip}&limit=${limit}`);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al obtener proyectos');
  }
};

export const createProject = async (data) => {
  try {
    return await apiClient.post('/projects', data);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al crear proyecto');
  }
};

export const getProject = async (projectId) => {
  try {
    return await apiClient.get(`/projects/${projectId}`);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al obtener proyecto');
  }
};

export const updateProject = async (projectId, data) => {
  try {
    return await apiClient.put(`/projects/${projectId}`, data);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al actualizar proyecto');
  }
};

export const deleteProject = async (projectId) => {
  try {
    return await apiClient.delete(`/projects/${projectId}`);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al eliminar proyecto');
  }
};

export const getProjectMembers = async (projectId) => {
  try {
    return await apiClient.get(`/projects/${projectId}/members`);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al obtener miembros');
  }
};

export const addProjectMember = async (projectId, userId) => {
  try {
    return await apiClient.post(`/projects/${projectId}/members`, { user_id: userId });
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al agregar miembro');
  }
};

export const removeProjectMember = async (projectId, userId) => {
  try {
    return await apiClient.delete(`/projects/${projectId}/members/${userId}`);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al eliminar miembro');
  }
};
