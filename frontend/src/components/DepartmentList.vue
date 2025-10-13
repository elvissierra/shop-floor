<template>
  <div class="department-list">
    <h2>Departments</h2>
    <div class="toolbar">
      <button class="btn-primary" @click="openCreate">+ Add Department</button>
      <div class="spacer"></div>
      <input
        v-model.trim="q"
        @keydown.enter.prevent
        type="search"
        class="search"
        placeholder="Search departments…"
        aria-label="Search departments"
      />
      <select v-model="sortKey" class="sort" aria-label="Sort departments">
        <option value="alpha">A → Z</option>
        <option value="recent">Newest first</option>
      </select>
    </div>
      <div v-if="loading" class="skeletons">
        <div class="sk-card" v-for="n in 6" :key="n"></div>
      </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="departments">
      <div v-for="dept in visibleDepartments" :key="dept.id" class="department-card">
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
    <Modal v-if="showModal" @cancel="closeModal">
      <template #title>{{ editing ? 'Edit Department' : 'New Department' }}</template>
      <DepartmentForm v-model="form" :submitting="submitting" @cancel="closeModal" @submit="saveDepartment" />
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';
import { useToast } from '../composables/useToast'
import Modal from './Modal.vue'
import DepartmentForm from './DepartmentForm.vue'
import { shopFloorService } from '../services/api'

const { push: toast } = useToast()
const store = useShopFloorStore();
const departments = ref([]);
const loading = ref(true);
const error = ref(null);
const limit = ref(20);
const offset = ref(0);
const moreAvailable = ref(true);

const q = ref('');
const sortKey = ref('recent');
const visibleDepartments = computed(() => {
  let list = departments.value;
  if (q.value) {
    const needle = q.value.toLowerCase();
    list = list.filter(d =>
      d.title?.toLowerCase().includes(needle) ||
      d.description?.toLowerCase().includes(needle)
    );
  }
  if (sortKey.value === 'alpha') {
    list = [...list].sort((a,b) => a.title.localeCompare(b.title));
  } else {
    // assume higher id == newer as a simple heuristic
    list = [...list].sort((a,b) => (b.id ?? 0) - (a.id ?? 0));
  }
  return list;
});

const showModal = ref(false)
const editing = ref(false)
const submitting = ref(false)
const form = ref({ title: '', description: '' })
const selectedId = ref(null)

function openCreate() {
  editing.value = false
  form.value = { title: '', description: '' }
  showModal.value = true
}
function openEdit(dept) {
  editing.value = true
  form.value = { title: dept.title, description: dept.description }
  selectedId.value = dept.id
  showModal.value = true
}
function closeModal() { showModal.value = false }

async function saveDepartment() {
  try {
    submitting.value = true
    if (editing.value && selectedId.value != null) {
      const updated = await shopFloorService.updateDepartment(selectedId.value, form.value)
      const idx = departments.value.findIndex(d => d.id === selectedId.value)
      if (idx !== -1) departments.value[idx] = updated
      toast({ type: 'success', title: 'Department updated', message: updated.title })
    } else {
      const created = await shopFloorService.createDepartment(form.value)
      departments.value.unshift(created)
      toast({ type: 'success', title: 'Department created', message: created.title })
    }
    closeModal()
  } catch (err) {
    error.value = err.message
    toast({ type: 'error', title: 'Save failed', message: err.code ? `${err.code}: ${err.message}` : err.message })
  } finally {
    submitting.value = false
  }
}

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

const editDepartment = (dept) => openEdit(dept)

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
.toolbar { display:flex; align-items:center; gap:.5rem; margin-top:.5rem; }
.toolbar .spacer { flex:1; }
.search { border:1px solid #d1d5db; border-radius:8px; padding:.45rem .6rem; min-width: 220px; }
.sort { border:1px solid #d1d5db; border-radius:8px; padding:.45rem .6rem; background:#fff; }
.btn-primary { background:#2563eb; color:#fff; border:none; border-radius:8px; padding:.5rem .9rem; cursor:pointer; }
.btn-primary:hover { opacity:.95; }
.department-card { transition: box-shadow .15s ease, transform .15s ease; }
.department-card:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(0,0,0,.08); }