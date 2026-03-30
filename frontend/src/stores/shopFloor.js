import { defineStore } from 'pinia';
import { fetchGraphQL } from '../services/graphql';

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
        const data = await fetchGraphQL(`
          query DashboardData {
            departments { id title description }
            workCenters { id name code departmentId }
            parts { id name departmentId }
          }
        `);
        this.shopFloorData = {
          departments: data.departments ?? [],
          workCenters: data.workCenters ?? [],
          parts: data.parts ?? [],
        };
        this.error = null;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
  },
});
