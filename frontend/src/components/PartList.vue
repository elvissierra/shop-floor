<template>
  <div class="part-list">
    <PageHeader title="Parts" :subtitle="`${parts.length} total`">
      <template #actions>
        <button class="btn-primary" @click="openCreate">+ Add Part</button>
      </template>
    </PageHeader>

    <div class="toolbar">
      <div class="spacer"></div>
      <input
        v-model.trim="q"
        @keydown.enter.prevent
        type="search"
        class="search"
        placeholder="Search parts…"
        aria-label="Search parts"
      />
    </div>

    <div v-if="loading" class="skeletons">
      <div class="sk-card" v-for="n in 6" :key="n"></div>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="parts">
      <div
        v-for="part in visibleParts"
        :key="part.id"
        class="part-card"
        tabindex="0"
        role="button"
        @click="openEdit(part)"
        @keydown.enter.prevent="openEdit(part)"
        @keydown.space.prevent="openEdit(part)"
        :aria-label="`Edit part ${part.name}`"
      >
        <h3>{{ part.name }}</h3>
        <p>Department ID: {{ part.departmentId }}</p>
        <div class="part-actions">
          <button @click="viewQuality(part)" class="btn-view">View Quality</button>
          <button @click="addDefect(part)" class="btn-add">Add Defect</button>
        </div>
      </div>
    </div>

    <div v-if="!loading && !error && parts.length === 0" class="empty">
      <h3>No parts yet</h3>
      <p>Add parts via the GraphQL mutation and they will appear here.</p>
      <button class="btn-more" @click="loadBatch(true)">Refresh</button>
    </div>

    <div v-if="!loading" class="pager">
      <button v-if="moreAvailable" @click="loadBatch()" class="btn-more">Load more</button>
      <div v-else class="end">No more parts</div>
    </div>

    <Modal v-if="showModal" @cancel="closeModal">
      <template #title>{{ editing ? 'Edit Part' : 'New Part' }}</template>
      <form class="form" @submit.prevent="savePart">
        <div class="field">
          <label for="pname">Name <span class="req">*</span></label>
          <input id="pname" v-model.trim="form.name" type="text" required :disabled="submitting" autocomplete="off" />
        </div>
        <div class="field">
          <label for="pdept">Department</label>
          <select id="pdept" v-model.number="form.departmentId" :disabled="submitting">
            <option v-for="d in departmentOptions" :key="d.id" :value="d.id">{{ d.title }}</option>
          </select>
        </div>
        <div class="actions">
          <button type="button" class="btn" @click="closeModal" :disabled="submitting">Cancel</button>
          <button type="submit" class="btn primary" :disabled="submitting || !form.name">
            <span v-if="submitting">Saving…</span>
            <span v-else>Save</span>
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';
import { useToast } from '../composables/useToast'
import Modal from './Modal.vue'
import PageHeader from './PageHeader.vue'

const { push: toast } = useToast()
const store = useShopFloorStore();
const parts = ref([]);
const loading = ref(true);
const error = ref(null);
const limit = ref(20);
const offset = ref(0);
const moreAvailable = ref(true);

const q = ref('');
const visibleParts = computed(() => {
  if (!q.value) return parts.value;
  const needle = q.value.toLowerCase();
  return parts.value.filter(p =>
    p.name?.toLowerCase().includes(needle) ||
    String(p.departmentId ?? '').includes(needle)
  );
});

const showModal = ref(false)
const editing = ref(false)
const submitting = ref(false)
const form = ref({ name: '', departmentId: null })
const departmentOptions = ref([])
const selectedId = ref(null)

function openCreate() {
  editing.value = false
  form.value = { name: '', departmentId: departmentOptions.value[0]?.id ?? null }
  showModal.value = true
}
function openEdit(part) {
  editing.value = true
  form.value = { name: part.name, departmentId: part.departmentId }
  selectedId.value = part.id
  showModal.value = true
}
function closeModal() { showModal.value = false }

async function savePart() {
  try {
    submitting.value = true
    if (editing.value && selectedId.value != null) {
      const updated = await store.updatePart(selectedId.value, form.value)
      const idx = parts.value.findIndex(p => p.id === selectedId.value)
      if (idx !== -1) parts.value[idx] = updated
      toast({ type: 'success', title: 'Part updated', message: updated.name })
    } else {
      const created = await store.addPart(form.value)
      parts.value.unshift(created)
      toast({ type: 'success', title: 'Part created', message: created.name })
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
    parts.value = [];
    offset.value = 0;
    moreAvailable.value = true;
  }
  try {
    const batch = await store.fetchParts({ limit: limit.value, offset: offset.value });
    if (!batch || batch.length === 0) {
      moreAvailable.value = false;
      return;
    }
    parts.value = parts.value.concat(batch);
    offset.value += batch.length;
  } catch (err) {
    error.value = err.message;
    toast({ type: 'error', title: 'Load failed', message: err.code ? `${err.code}: ${err.message}` : err.message })
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await loadBatch(true);
  try {
    departmentOptions.value = await store.fetchDepartments({ limit: 100 });
  } catch (e) {
    // ignore; parts page still works without options
  }
});

const viewQuality = (part) => {
  console.log('View quality for part:', part);
};

const addDefect = (part) => {
  console.log('Add defect for part:', part);
};
</script>

<style scoped>

.parts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

@media (min-width: 1280px) {
  .parts { gap: 1.25rem; }
  .search { min-width: 280px; }
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

.part-card:focus { outline:none; box-shadow:0 0 0 3px rgba(37,99,235,.35); }

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
  background-color: var(--c-accent);
  color: white;
}

.btn-add {
  background-color: #1f2937;
  color: white;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: var(--c-danger-600);
  padding: 1rem;
  border: 1px solid var(--c-danger-600);
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
.toolbar { display:flex; align-items:center; gap:.5rem; margin-top:.5rem; }
.toolbar .spacer { flex:1; }
.search { border:1px solid #d1d5db; border-radius:8px; padding:.45rem .6rem; min-width: 220px; }
.part-card { transition: box-shadow .15s ease, transform .15s ease; }
.part-card:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(0,0,0,.08); }
.btn-primary { background: var(--c-primary); color:#fff; border:none; border-radius:8px; padding:.5rem .9rem; cursor:pointer; }
.btn-primary:hover { opacity:.95; }
.form { display:flex; flex-direction:column; gap:.75rem; }
.field { display:flex; flex-direction:column; gap:.25rem; }
.req { color: var(--c-danger-600); }
input, select { border:1px solid var(--c-border); border-radius:8px; padding:.5rem .6rem; background:#fff; }
.actions { display:flex; justify-content:flex-end; gap:.5rem; margin-top:.5rem; }
.btn { border:none; border-radius:8px; padding:.5rem .9rem; cursor:pointer; background:#e5e7eb; }
.btn.primary { background: var(--c-primary); color:#fff; }
</style>