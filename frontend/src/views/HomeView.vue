<template>
  <section class="home">
    <div class="hero" role="banner" aria-label="Shop Floor hero">
      <h1 class="hero-title">Dashboard</h1>
      <p class="hero-sub">
        High-level view of your departments, work centers, and parts.
      </p>
      <div class="hero-actions">
        <router-link to="/departments" class="btn btn-primary">View Departments</router-link>
        <router-link to="/parts" class="btn btn-outline">Manage Parts</router-link>
      </div>
    </div>

    <div class="kpis">
      <div class="kpi card">
        <div class="kpi-num">{{ deptCount }}</div>
        <div class="kpi-label">Departments</div>
      </div>
      <div class="kpi card">
        <div class="kpi-num">{{ workCenterCount }}</div>
        <div class="kpi-label">Work Centers</div>
      </div>
      <div class="kpi card">
        <div class="kpi-num">{{ partCount }}</div>
        <div class="kpi-label">Parts</div>
      </div>
    </div>

    <div class="latest">
      <h2 class="h2">Latest Parts</h2>
      <div class="list">
        <div v-if="loadingLatest" class="skeleton-list">
          <div class="skeleton card" v-for="n in 5" :key="n"></div>
        </div>
        <template v-else>
          <div v-if="latestParts.length === 0" class="muted">No parts yet.</div>
          <div v-for="p in latestParts" :key="p.id" class="row card">
            <div class="row-main">
              <div class="row-title">{{ p.name }}</div>
              <div class="row-sub">
                Dept:
                <span class="badge">
                  {{ departmentLabelForPart(p) }}
                </span>
              </div>
            </div>
            <router-link class="row-cta" to="/parts">Open</router-link>
          </div>
        </template>
      </div>
    </div>

    <div class="feature-grid">
      <div class="card feature">
        <h3 class="feature-title">Quick Updates</h3>
        <p class="feature-text">Add, edit, and find departments and parts in a few clicks with instant feedback.</p>
      </div>
      <div class="card feature">
        <h3 class="feature-title">Accurate Shop Data</h3>
        <p class="feature-text">Keep your departments, work centers, and parts in sync so everyone is working from the same source of truth.</p>
      </div>
      <div class="card feature">
        <h3 class="feature-title">Floor Overview</h3>
        <p class="feature-text">
          Use the shop floor map to see where departments and work centers live in the plant and jump into their details.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useShopFloorStore } from '../stores/shopFloor'
import { ref } from 'vue'
import { shopFloorService } from '../services/api'


const store = useShopFloorStore()
onMounted(() => { if (!store.shopFloorData) store.fetchShopFloorData() })
const deptCount = computed(() => store.shopFloorData?.departments?.length ?? 0)
const workCenterCount = computed(() => store.shopFloorData?.workCenters?.length ?? 0)
const partCount = computed(() => store.shopFloorData?.parts?.length ?? 0)

const departmentLookup = computed(() => {
  const map = new Map()
  const departments = store.shopFloorData?.departments ?? []
  for (const d of departments) {
    if (d && typeof d.id !== 'undefined') {
      map.set(d.id, d.title ?? d.name ?? String(d.id))
    }
  }
  return map
})

function departmentLabelForPart(p) {
  if (!p || p.departmentId == null) return '—'
  return departmentLookup.value.get(p.departmentId) ?? `#${p.departmentId}`
}
const latestParts = ref([])
const loadingLatest = ref(false)

onMounted(async () => {
  loadingLatest.value = true
  try {
    latestParts.value = await shopFloorService.getParts({ limit: 5, offset: 0 })
  } finally {
    loadingLatest.value = false
  }
})
</script>

<style scoped>
.hero{
  border-radius:var(--radius);
  padding:2.5rem 2rem;
  margin-bottom:1rem;
  background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 45%,#0ea5e9 100%);
  color:#fff;
  box-shadow:var(--shadow);
}
.hero-title{font-size:2.4rem;line-height:1.1;font-weight:900;margin:0 0 .5rem 0;letter-spacing:.2px;}
.hero-sub{font-size:1.05rem;opacity:.95;margin:0 0 1rem 0;max-width:68ch;}
.hero-actions{display:flex;gap:.75rem;flex-wrap:wrap;}

.kpis{display:grid;grid-template-columns:repeat(3,minmax(220px,1fr));gap:.9rem;margin:1rem 0 1.25rem 0;}
.card{background:var(--c-surface);border:1px solid var(--c-border);border-radius:var(--radius);box-shadow:var(--shadow);padding:1rem;}
.kpi-num{font-size:2rem;font-weight:900;color:var(--c-text);line-height:1.1;}
.kpi-label{margin-top:.25rem;color:var(--c-muted);}

.feature-grid{display:grid;grid-template-columns:repeat(3,minmax(260px,1fr));gap:.9rem;}
.feature-title{margin:0 0 .25rem 0;font-weight:800;color:var(--c-text);}
.feature-text{margin:0;color:var(--c-muted);font-size:.98rem;}

@media (max-width:1200px){
  .kpis{grid-template-columns:repeat(2,minmax(240px,1fr));}
  .feature-grid{grid-template-columns:repeat(2,minmax(240px,1fr));}
  .hero-title{font-size:2rem;}
}
@media (max-width:800px){
  .kpis{grid-template-columns:1fr;}
  .feature-grid{grid-template-columns:1fr;}
}

.h2{margin:.25rem 0 .5rem 0;font-size:1.05rem;color:var(--c-muted);font-weight:800;letter-spacing:.2px;text-transform:uppercase;}
.list{display:flex;flex-direction:column;gap:.5rem;}
.row{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.75rem .85rem;}
.row-title{font-weight:800;}
.row-sub{color:var(--c-muted);font-size:.92rem;}
.row-cta{white-space:nowrap;text-decoration:none;border:1px solid var(--c-border);padding:.35rem .6rem;border-radius:.5rem;}
.muted{color:var(--c-muted);}
.badge{display:inline-block;padding:.1rem .4rem;border:1px solid var(--c-border);border-radius:.4rem;}

/* skeleton shimmer */
.skeleton{height:58px;border-radius:var(--radius);background:linear-gradient(90deg, rgba(0,0,0,.06), rgba(0,0,0,.12), rgba(0,0,0,.06));background-size:200% 100%;animation:shimmer 1.1s infinite;}
.skeleton-list .skeleton{margin-bottom:.5rem;}
@keyframes shimmer{0%{background-position:200% 0;}100%{background-position:-200% 0;}}
</style>