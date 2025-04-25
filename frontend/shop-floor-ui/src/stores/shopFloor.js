import { defineStore } from 'pinia';
import { shopFloorService } from '../services/api';

export const useShopFloorStore = defineStore('shopFloor', {
  state: () => ({
    shopFloorData: null,
    loading: false,
    error: null,
  }),
  
  actions: {
    async fetchShopFloorData() {
      this.loading = true;
      try {
        this.shopFloorData = await shopFloorService.getShopFloorData();
        this.error = null;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    
    async updateShopFloorData(data) {
      this.loading = true;
      try {
        const updatedData = await shopFloorService.updateShopFloorData(data);
        this.shopFloorData = updatedData;
        this.error = null;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
  },
}); 