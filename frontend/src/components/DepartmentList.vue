<template>
  <div class="department-list">
    <h2>Departments</h2>
    <div class="toolbar">
      <button class="btn-primary" @click="openCreate">+ Add Department</button>
    </div>
      <div v-if="loading" class="skeletons">
        <div class="sk-card" v-for="n in 6" :key="n"></div>
      </div>
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
    <div v-if="!loading && !error && departments.length === 0" class="empty">
      <h3>No departments yet</h3>
      <p>Create your first department from the backend or via GraphQL.</p>
      <button class="btn-more" @click="loadBatch(true)">Refresh</button>
    </div>
    <div v-if="!loading" class="pager">
    <button v-if="moreAvailable" @click="loadBatch()" class="btn-more">Load more</button>
    <div v-else class="end">No more departments</div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';
import { useToast } from '../composables/useToast'

const { push: toast } = useToast()
const store = useShopFloorStore();
const departments = ref([]);
const loading = ref(true);
const error = ref(null);
const limit = ref(20);
const offset = ref(0);
const moreAvailable = ref(true);

async function loadBatch(reset = false) {
  if (reset) {
    departments.value = [];
    offset.value = 0;
    moreAvailable.value = true;
  }
  try {
    const batch = await store.fetchDepartments({ limit: limit.value, offset: offset.value });
    if (!batch || batch.length === 0) {
      moreAvailable.value = false;
      return;
    }
    departments.value = departments.value.concat(batch);
    offset.value += batch.length;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

onMounted(() => { loadBatch(true); });

const editDepartment = (dept) => {
  // TODO: Implement edit functionality
  console.log('Edit department:', dept);
};

const deleteDepartment = async (id) => {
  if (confirm('Are you sure you want to delete this department?')) {
    try {
      await store.deleteDepartment(id);
      departments.value = departments.value.filter(d => d.id !== id);
      toast({ type: 'success', title: 'Department deleted', message: 'The department was removed.' })
    } catch (err) {
      error.value = err.message;
      toast({ type: 'error', title: 'Delete failed', message: err.code ? `${err.code}: ${err.message}` : err.message })
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

.pager { margin-top: 1rem; display:flex; justify-content:center; }
.btn-more { background:#2c3e50; color:#fff; border:none; border-radius:6px; padding:0.6rem 1rem; cursor:pointer; }
.btn-more:hover { opacity: .9; }
.end { color:#888; font-size:.9rem; }

.skeletons { display:grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap:1rem; margin-top:1rem; }
.sk-card { height: 120px; border-radius:8px; background: linear-gradient(90deg, #eee 25%, #f5f5f5 37%, #eee 63%); background-size: 400% 100%; animation: shimmer 1.2s ease-in-out infinite; }
@keyframes shimmer { 0% { background-position: 100% 0; } 100% { background-position: -100% 0; } }
.empty { text-align:center; padding: 2rem 0; color:#555; }
.empty h3 { margin:0 0 .5rem 0; color:#2c3e50; }
</style> 