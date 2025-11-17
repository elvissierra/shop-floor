<template>
  <section class="sf container">
    <div class="sf-hero card">
      <div>
        <h1 class="title">Operations Hub</h1>
        <p class="sub">Your jumping-off point for departments, parts, and day-to-day actions.</p>
      </div>
      <div class="actions">
        <router-link to="/departments" class="btn btn-primary">Go to Departments</router-link>
        <router-link to="/parts" class="btn">Go to Parts</router-link>
      </div>
    </div>

    <div class="grid">
      <div class="col">
        <h2 class="h2">Departments Preview</h2>
        <div class="list">
          <div v-if="loadingDept" class="muted">Loading…</div>
          <template v-else>
            <div v-if="departments.length === 0" class="muted">No departments yet.</div>
            <div v-for="d in departments" :key="d.id" class="row card">
              <div class="row-main">
                <div class="row-title">{{ d.title }}</div>
                <div class="row-sub">{{ d.description || '—' }}</div>
              </div>
              <router-link class="row-cta" :to="`/departments`">Open</router-link>
            </div>
          </template>
        </div>
      </div>

      <div class="col">
        <h2 class="h2">Recent Parts</h2>
        <div class="list">
          <div v-if="loadingParts" class="muted">Loading…</div>
          <template v-else>
            <div v-if="parts.length === 0" class="muted">No parts yet.</div>
            <div v-for="p in parts" :key="p.id" class="row card">
              <div class="row-main">
                <div class="row-title">{{ p.name }}</div>
                <div class="row-sub">Dept: <span class="badge">{{ p.departmentId ?? '—' }}</span></div>
              </div>
              <router-link class="row-cta" :to="`/parts`">Open</router-link>
            </div>
          </template>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useShopFloorStore } from '../stores/shopFloor'

const store = useShopFloorStore()
const loadingDept = ref(false)
const loadingParts = ref(false)
const departments = ref([])
const parts = ref([])

onMounted(async () => {
  loadingDept.value = true
  try { departments.value = await store.fetchDepartments({ limit: 4, offset: 0 }) }
  finally { loadingDept.value = false }

  loadingParts.value = true
  try { parts.value = await store.fetchParts({ limit: 5, offset: 0 }) }
  finally { loadingParts.value = false }
})
</script>

<style scoped>
.sf-hero{
  display:flex;align-items:center;justify-content:space-between;gap:1rem;
  margin:.5rem 0 1rem 0;padding:1rem 1.25rem;
  background:var(--c-surface);border:1px solid var(--c-border);
  border-radius:var(--radius);box-shadow:var(--shadow);
}
.title{margin:0;font-size:1.6rem;font-weight:900;color:var(--c-text);}
.sub{margin:.25rem 0 0 0;color:var(--c-muted);max-width:72ch;}
.actions{display:flex;gap:.5rem;flex-wrap:wrap;}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
.h2{margin:.25rem 0 .5rem 0;font-size:1.05rem;color:var(--c-muted);font-weight:800;letter-spacing:.2px;text-transform:uppercase;}
.list{display:flex;flex-direction:column;gap:.5rem;}
.row{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.75rem .85rem;}
.row-title{font-weight:800;}
.row-sub{color:var(--c-muted);font-size:.92rem;}
.row-cta{white-space:nowrap;text-decoration:none;border:1px solid var(--c-border);padding:.35rem .6rem;border-radius:.5rem;}
.muted{color:var(--c-muted);}
.badge{display:inline-block;padding:.1rem .4rem;border:1px solid var(--c-border);border-radius:.4rem;}
@media (max-width:1100px){ .grid{grid-template-columns:1fr;} }
.card{
  background:var(--c-surface);border:1px solid var(--c-border);
  border-radius:var(--radius);box-shadow:var(--shadow);
}
</style>