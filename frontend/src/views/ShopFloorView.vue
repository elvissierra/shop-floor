
// Store is wired to GraphQL (fetchShopFloorData() → services/api.js → /graphql)

<template>
  <div class="shop-floor">
    <h1>Shop Floor Dashboard</h1>
    
    <div v-if="loading" class="loading">
      Loading...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else-if="shopFloorData" class="dashboard">
      <!-- Add your shop floor visualization components here -->
      <div class="data-display">
        <pre>{{ JSON.stringify(shopFloorData, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';

const store = useShopFloorStore();

onMounted(() => {
  store.fetchShopFloorData();
});

const { shopFloorData, loading, error } = store;
</script>

<style scoped>
.shop-floor {
  padding: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.error {
  color: #dc3545;
  padding: 1rem;
  border: 1px solid #dc3545;
  border-radius: 4px;
  margin: 1rem 0;
}

.dashboard {
  display: grid;
  gap: 2rem;
}

.data-display {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}
</style> 