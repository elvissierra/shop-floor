import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const shopFloorService = {
  // Department methods
  async getDepartments() {
    const response = await api.get('/departments');
    return response.data;
  },

  async createDepartment(departmentData) {
    const response = await api.post('/departments', departmentData);
    return response.data;
  },

  async deleteDepartment(id) {
    const response = await api.delete(`/departments/${id}`);
    return response.data;
  },

  // Part methods
  async getParts() {
    const response = await api.get('/parts');
    return response.data;
  },

  async createPart(partData) {
    const response = await api.post('/parts', partData);
    return response.data;
  },

  // Quality methods
  async getQuality(partId) {
    const response = await api.get(`/quality/${partId}`);
    return response.data;
  },
};

export default api; 