<template>
  <div class="part-list">
    <h2>Parts</h2>
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
      <div v-for="part in visibleParts" :key="part.id" class="part-card">
        <h3>{{ part.name }}</h3>
        <p>Department ID: {{ part.department_id }}</p>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';
import { useToast } from '../composables/useToast'

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
    String(p.department_id ?? '').includes(needle)
  );
});

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

onMounted(() => { loadBatch(true); });

const viewQuality = (part) => {
  console.log('View quality for part:', part);
};

const addDefect = (part) => {
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
.part-card { transition: box-shadow .15s ease, transform .15s ease; }
.part-card:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(0,0,0,.08); }