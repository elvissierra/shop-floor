import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Update this to match your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export const shopFloorService = {
  // Department methods
  async getDepartments() {
    const response = await api.get('/api/departments');
    return response.data;
  },

  async deleteDepartment(id) {
    const response = await api.delete(`/api/departments/${id}`);
    return response.data;
  },

  // Part methods
  async getParts() {
    const response = await api.get('/api/parts');
    return response.data;
  },

  async addPart(partData) {
    const response = await api.post('/api/parts', partData);
    return response.data;
  },

  // Quality methods
  async getQuality(partId) {
    const response = await api.get(`/api/quality/${partId}`);
    return response.data;
  },

  // Defect methods
  async addDefect(defectData) {
    const response = await api.post('/api/defects', defectData);
    return response.data;
  },

  // Add your API methods here
  async getShopFloorData() {
    const response = await api.get('/api/shop-floor');
    return response.data;
  },
  
  async updateShopFloorData(data) {
    const response = await api.put('/api/shop-floor', data);
    return response.data;
  }
};

export default api; 