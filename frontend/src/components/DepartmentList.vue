
// store needs to be reconfigured to use Gql// store now uses GraphQL service

<template>
  <div class="department-list">
    <h2>Departments</h2>
    <div v-if="loading" class="loading">Loading departments...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="departments">
      <div v-for="dept in departments" :key="dept.id" class="department-card">
        <h3>{{ dept.title }}</h3>
        <p>{{ dept.description }}</p>
        <div class="department-actions">
          <button @click="editDepartment(dept)" class="btn-edit">Edit</button>
          <button @click="deleteDepartment(dept.id)" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';

const store = useShopFloorStore();
const departments = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await store.fetchDepartments();
    departments.value = response;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

const editDepartment = (dept) => {
  // TODO: Implement edit functionality
  console.log('Edit department:', dept);
};

const deleteDepartment = async (id) => {
  if (confirm('Are you sure you want to delete this department?')) {
    try {
      await store.deleteDepartment(id);
      departments.value = departments.value.filter(d => d.id !== id);
    } catch (err) {
      error.value = err.message;
    }
  }
};
</script>

<style scoped>
.department-list {
  padding: 1rem;
}

.departments {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.department-card {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.department-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.department-card p {
  margin: 0 0 1rem 0;
  color: #666;
}

.department-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-edit {
  background-color: #42b983;
  color: white;
}

.btn-delete {
  background-color: #dc3545;
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