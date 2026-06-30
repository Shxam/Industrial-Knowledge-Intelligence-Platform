import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
});

// Request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Document APIs
export const documents = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  status: (documentId: string) => api.get(`/documents/${documentId}/status`),
  delete: (documentId: string) => api.delete(`/documents/${documentId}`),
  list: () => api.get('/documents'),
};

// Query APIs
export const query = {
  ask: (question: string, strategy: 'vector' | 'bm25' | 'hybrid' = 'hybrid') =>
    api.post('/query', { question, query: question, strategy, stream: false }),
};

// RCA APIs
export const rca = {
  analyze: (failureDescription: string) =>
    api.post('/rca/analyze', { failure_description: failureDescription }),
};

// Graph APIs
export const graph = {
  stats: () => api.get('/graph/stats'),
  visualize: (limit: number = 100) => api.get(`/graph/visualize?limit=${limit}`),
  search: (entityName: string) => api.get(`/graph/search?entity_name=${entityName}`),
};

export default api;
