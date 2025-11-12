import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  healthCheck: () => api.get('/api/health'),

  // Dashboard
  getDashboard: () => api.get('/api/dashboard'),

  // Equipamentos
  getEquipmentDetails: (id) => api.get(`/api/equipment/${id}`),
  getEquipmentSensors: (id) => api.get(`/api/equipment/${id}/sensors`),
  simulateReadings: (id) => api.post(`/api/equipment/${id}/simulate`),

  // Alertas
  getAlerts: (params = {}) => api.get('/api/alerts', { params }),
  acknowledgeAlert: (id, user) => api.post(`/api/alert/${id}/acknowledge`, { user }),

  // Inicialização
  initSampleData: () => api.post('/api/init-data'),
};

export default api;