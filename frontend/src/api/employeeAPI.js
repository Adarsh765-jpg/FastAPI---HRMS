/**
 * Employee API endpoints
 */
import apiClient from './axiosClient';

export const employeeAPI = {
  // Get all employees with filters and pagination
  getAll: (params = {}) => {
    return apiClient.get('/employees/', { params });
  },

  // Get single employee by ID
  getById: (id) => {
    return apiClient.get(`/employees/${id}`);
  },

  // Create new employee
  create: (data) => {
    return apiClient.post('/employees/', data);
  },

  // Update employee
  update: (id, data) => {
    return apiClient.put(`/employees/${id}`, data);
  },

  // Delete employee
  delete: (id) => {
    return apiClient.delete(`/employees/${id}`);
  },
};

export const authAPI = {
  // Login
  login: (credentials) => {
    return apiClient.post('/auth/login', credentials);
  },

  // Get current user profile
  getProfile: () => {
    return apiClient.get('/me');
  },
};
