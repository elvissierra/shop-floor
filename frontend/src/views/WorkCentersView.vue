<template>
  <section class="wc container">
    <div class="wc-hero card">
      <div>
        <h1 class="title">Work Centers</h1>
        <p class="sub">
          Manage the work centers that own operations on the shop floor.
        </p>
      </div>
      <div class="actions">
        <button class="btn btn-primary" type="button" @click="toggleForm">
          {{ showForm ? 'Close form' : 'Add Work Center' }}
        </button>
      </div>
    </div>

    <div v-if="showForm" class="card wc-form">
      <h2 class="h2">New Work Center</h2>
      <form @submit.prevent="handleSubmit" class="form-grid">
        <div class="field">
          <label class="label" for="name">Name</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            class="input"
            required
            placeholder="Assembly Line 1"
          />
        </div>

        <div class="field">
          <label class="label" for="code">Code</label>
          <input
            id="code"
            v-model="form.code"
            type="text"
            class="input"
            placeholder="WC-10"
          />
        </div>

        <div class="field">
          <label class="label" for="dept">Department</label>
          <select
            id="dept"
            v-model="form.departmentId"
            class="input"
          >
            <option :value="null">No department</option>
            <option
              v-for="d in departments"
              :key="d.id"
              :value="d.id"
            >
              {{ d.title }}
            </option>
          </select>
        </div>

        <div class="field actions-row">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="saving || !form.name.trim()"
          >
            {{ saving ? 'Saving…' : 'Save Work Center' }}
          </button>
          <button type="button" class="btn btn-ghost" @click="resetForm">
            Clear
          </button>
        </div>
      </form>
    </div>

    <div class="card wc-table">
      <div class="wc-table-header">
        <h2 class="h2">All Work Centers</h2>
        <div class="muted small">
          {{ centers.length }} total
        </div>
      </div>

      <div v-if="loading" class="muted">Loading…</div>
      <div v-else-if="centers.length === 0" class="muted">
        No work centers yet.
      </div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Code</th>
            <th>Department</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wc in centers" :key="wc.id">
            <td>{{ wc.name }}</td>
            <td>
              <span v-if="wc.code" class="badge">{{ wc.code }}</span>
              <span v-else class="muted">—</span>
            </td>
            <td>
              <span class="badge">
                {{ departmentLabel(wc.departmentId) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useShopFloorStore } from '../stores/shopFloor'

const store = useShopFloorStore()

const centers = ref([])
const departments = ref([])
const loading = ref(false)
const showForm = ref(false)
const saving = ref(false)

const form = ref({
  name: '',
  code: '',
  departmentId: null,
})

const toggleForm = () => {
  showForm.value = !showForm.value
}

const resetForm = () => {
  form.value = {
    name: '',
    code: '',
    departmentId: null,
  }
}

const departmentLabel = (deptId) => {
  if (!deptId) return 'Unassigned'
  const d = departments.value.find(d => d.id === deptId)
  return d ? d.title : `Dept ${deptId}`
}

const handleSubmit = async () => {
  if (!form.value.name.trim()) return
  saving.value = true
  try {
    const payload = {
      name: form.value.name.trim(),
      code: form.value.code || null,
      departmentId: form.value.departmentId
        ? Number(form.value.departmentId)
        : null,
    }
    const created = await store.addWorkCenter(payload)
    // prepend newly created center into the list
    centers.value = [created, ...centers.value]
    resetForm()
    showForm.value = false
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const [wcList, deptList] = await Promise.all([
      store.fetchWorkCenters({ limit: 100, offset: 0 }),
      store.fetchDepartments({ limit: 100, offset: 0 }),
    ])
    centers.value = wcList
    departments.value = deptList
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.wc-hero{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1rem;
  margin:.5rem 0 1rem 0;
  padding:1rem 1.25rem;
  background:var(--c-surface);
  border:1px solid var(--c-border);
  border-radius:var(--radius);
  box-shadow:var(--shadow);
}
.title{margin:0;font-size:1.6rem;font-weight:900;color:var(--c-text);}
.sub{margin:.25rem 0 0 0;color:var(--c-muted);max-width:72ch;}
.actions{display:flex;gap:.5rem;flex-wrap:wrap;}

.wc-form{margin-bottom:1rem;padding:1rem 1.25rem;}
.h2{margin:.25rem 0 .5rem 0;font-size:1.05rem;color:var(--c-muted);font-weight:800;letter-spacing:.2px;text-transform:uppercase;}

.form-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(220px,1fr));
  gap:.75rem 1rem;
  align-items:flex-end;
}
.field{display:flex;flex-direction:column;gap:.25rem;}
.label{font-size:.9rem;font-weight:600;color:var(--c-text);}
.input{
  border-radius:.5rem;
  border:1px solid var(--c-border);
  padding:.4rem .6rem;
  font-size:.95rem;
  background:var(--c-bg);
}
.actions-row{
  display:flex;
  gap:.5rem;
  justify-content:flex-start;
}

.wc-table{padding:1rem 1.25rem;}
.wc-table-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:.5rem;
}
.small{font-size:.85rem;}

.table{
  width:100%;
  border-collapse:collapse;
  font-size:.95rem;
}
.table th,
.table td{
  padding:.5rem .4rem;
  text-align:left;
  border-top:1px solid var(--c-border);
}
.table th{
  font-weight:700;
  color:var(--c-muted);
}

.badge{
  display:inline-block;
  padding:.1rem .4rem;
  border:1px solid var(--c-border);
  border-radius:.4rem;
}
.muted{color:var(--c-muted);}

@media (max-width:1100px){
  .form-grid{
    grid-template-columns:1fr;
  }
}
</style>