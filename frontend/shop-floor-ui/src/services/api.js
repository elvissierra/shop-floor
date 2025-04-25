import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Update this to match your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export const shopFloorService = {
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