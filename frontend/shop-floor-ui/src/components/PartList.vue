<template>
  <div class="part-list">
    <h2>Parts</h2>
    <div v-if="loading" class="loading">Loading parts...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="parts">
      <div v-for="part in parts" :key="part.id" class="part-card">
        <h3>{{ part.name }}</h3>
        <p>Department ID: {{ part.department_id }}</p>
        <div class="part-actions">
          <button @click="viewQuality(part)" class="btn-view">View Quality</button>
          <button @click="addDefect(part)" class="btn-add">Add Defect</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';

const store = useShopFloorStore();
const parts = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await store.fetchParts();
    parts.value = response;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

const viewQuality = (part) => {
  // TODO: Implement quality view
  console.log('View quality for part:', part);
};

const addDefect = (part) => {
  // TODO: Implement defect addition
  console.log('Add defect for part:', part);
};
</script>

<style scoped>
.part-list {
  padding: 1rem;
}

.parts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.part-card {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.part-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.part-card p {
  margin: 0 0 1rem 0;
  color: #666;
}

.part-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-view, .btn-add {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-view {
  background-color: #42b983;
  color: white;
}

.btn-add {
  background-color: #2c3e50;
  color: white;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #dc3545;
  padding: 1rem;
  border: 1px solid #dc3545;
  border-radius: 4px;
  margin: 1rem 0;
}
</style> 