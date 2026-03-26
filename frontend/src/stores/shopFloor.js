
// Store now uses GraphQL service under services/api.js (fetch to /graphql).

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
    
    // Department methods
    async fetchDepartments(params = {}) {
      this.loading = true;
      try {
        const response = await shopFloorService.getDepartments(params);
        this.error = null;
        return response;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async deleteDepartment(id) {
      this.loading = true;
      try {
        await shopFloorService.deleteDepartment(id);
        this.error = null;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // Work Center methods
    async fetchWorkCenters(params = {}) {
      this.loading = true;
      try {
        const response = await shopFloorService.getWorkCenters(params);
        this.error = null;
        return response;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async addWorkCenter(wcData) {
      this.loading = true;
      try {
        const response = await shopFloorService.createWorkCenter(wcData);
        this.error = null;
        return response;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // Part methods
    async fetchParts(params = {}) {
      this.loading = true;
      try {
        const response = await shopFloorService.getParts(params);
        this.error = null;
        return response;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async addPart(partData) {
      this.loading = true;
      try {
        const response = await shopFloorService.createPart(partData);
        this.error = null;
        return response;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async updatePart(id, partData) {
      this.loading = true;
      try {
        const response = await shopFloorService.updatePart(id, partData);
        this.error = null;
        return response;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
}); 