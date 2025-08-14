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
  updateThreatsRiskBatch,
  createThreatForSystem,
  updateThreatResidualRisk,
  updateThreatsResidualRiskBatch
} = threatService;

// Para mantener compatibilidad con código antiguo
export const getInformationSystemsById = informationSystemService.getInformationSystemById;

// También exportamos el cliente API y la URL base por si algún componente necesita acceso directo
export { apiClient, API_BASE_URL };

