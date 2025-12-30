<template>
  <section class="home">
    <!-- Top band: dashboard / quick glance -->
    <section class="home-top">
      <div class="hero" role="banner" aria-label="Shop Floor dashboard">
        <div class="hero-main">
          <p class="hero-overline">Structure & activity snapshot</p>
          <h1 class="hero-title">Operations dashboard</h1>
          <p class="hero-sub">
            At-a-glance view of active departments, work centers, and parts across your facility.
          </p>
          <div class="hero-actions">
            <router-link to="/departments" class="btn btn-primary">Review departments</router-link>
            <router-link to="/parts" class="btn btn-outline">Analyze parts</router-link>
          </div>
        </div>
        <div class="hero-panel" aria-label="Key counts for this facility">
          <div class="hero-metric">
            <span class="hero-metric-label">Departments</span>
            <span class="hero-metric-value">{{ deptCount }}</span>
          </div>
          <div class="hero-metric">
            <span class="hero-metric-label">Work centers</span>
            <span class="hero-metric-value">{{ workCenterCount }}</span>
          </div>
          <div class="hero-metric">
            <span class="hero-metric-label">Parts</span>
            <span class="hero-metric-value">{{ partCount }}</span>
          </div>
        </div>
      </div>

      <div class="kpis">
        <div class="kpi card">
          <div class="kpi-num">{{ deptCount }}</div>
          <div class="kpi-label">Active departments</div>
        </div>
        <div class="kpi card">
          <div class="kpi-num">{{ workCenterCount }}</div>
          <div class="kpi-label">Configured work centers</div>
        </div>
        <div class="kpi card">
          <div class="kpi-num">{{ partCount }}</div>
          <div class="kpi-label">Total parts in catalog</div>
        </div>
      </div>

      <div class="latest">
        <h2 class="h2">Latest parts activity</h2>
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
              <router-link
                class="row-cta"
                :to="{ name: 'part-detail', params: { id: p.id } }"
              >
                View part
              </router-link>
            </div>
          </template>
        </div>
      </div>
    </section>

    <!-- Middle band: guided object pages (CRUD and detail views) -->
    <section class="home-middle">
      <h2 class="section-title">Manage your shop data</h2>
      <p class="section-subtitle">
        Jump into the core pages where you define structure, maintain records, and review details.
      </p>
      <div class="middle-grid">
        <router-link to="/departments" class="card middle-card">
          <h3 class="middle-title">Departments</h3>
          <p class="middle-text">
            Define the main areas of your facility and see which work centers and parts belong in each.
          </p>
          <div class="middle-meta">
            <span class="middle-count">{{ deptCount }}</span>
            <span class="middle-label">active</span>
          </div>
        </router-link>

        <router-link to="/work-centers" class="card middle-card">
          <h3 class="middle-title">Work centers</h3>
          <p class="middle-text">
            Maintain the stations where work actually happens and track the orders flowing through them.
          </p>
          <div class="middle-meta">
            <span class="middle-count">{{ workCenterCount }}</span>
            <span class="middle-label">configured</span>
          </div>
        </router-link>

        <router-link to="/parts" class="card middle-card">
          <h3 class="middle-title">Parts catalog</h3>
          <p class="middle-text">
            Keep an organized list of the items you build or move, with links to their departments and routes.
          </p>
          <div class="middle-meta">
            <span class="middle-count">{{ partCount }}</span>
            <span class="middle-label">in catalog</span>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Bottom band: map layout + informational footer -->
    <section class="home-bottom">
      <div class="map-preview card">
        <div class="map-preview-main">
          <h2 class="h2">Floor map overview</h2>
          <p class="map-text">
            Use the shop floor map to place departments and work centers on a simple layout of your facility and
            jump directly into their detail pages.
          </p>
          <router-link to="/floor-map" class="btn btn-primary btn-map">Open floor map</router-link>
        </div>
        <div class="map-preview-legend" aria-label="Map legend">
          <div class="map-legend-row">
            <span class="map-swatch map-swatch-wc"></span>
            <span class="map-legend-label">Work center zones</span>
          </div>
          <div class="map-legend-row">
            <span class="map-swatch map-swatch-dept"></span>
            <span class="map-legend-label">Department zones</span>
          </div>
          <div class="map-legend-row">
            <span class="map-swatch map-swatch-other"></span>
            <span class="map-legend-label">Other areas</span>
          </div>
        </div>
      </div>

      <footer class="home-footer" aria-label="Dashboard summary information">
        <div class="feature-grid">
          <div class="card feature">
            <h3 class="feature-title">Quick updates</h3>
            <p class="feature-text">
              Add, edit, and find departments, work centers, and parts in a few clicks with instant feedback.
            </p>
          </div>
          <div class="card feature">
            <h3 class="feature-title">Accurate shop data</h3>
            <p class="feature-text">
              Keep your structure in sync so every team is working from the same source of truth.
            </p>
          </div>
          <div class="card feature">
            <h3 class="feature-title">Floor overview</h3>
            <p class="feature-text">
              Combine the floor map with your master data to see where work actually happens on the shop floor.
            </p>
          </div>
        </div>
      </footer>
    </section>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useShopFloorStore } from '../stores/shopFloor'
import { ref } from 'vue'
import { shopFloorService } from '../services/api'


const store = useShopFloorStore()

function safeCount(field) {
  const data = store.shopFloorData
  if (!data) return 0

  const value = (store.shopFloorData || {})[field]

  if (Array.isArray(value)) return value.length
  if (typeof value === 'number') return value
  if (value && typeof value === 'object' && typeof value.count === 'number') {
    return value.count
  }

  return 0
}
onMounted(() => {
  if (!store.shopFloorData) {
    store.fetchShopFloorData()
  }
})

const deptCount = computed(() => safeCount('departments'))
const workCenterCount = computed(() => safeCount('workCenters'))
const partCount = computed(() => safeCount('parts'))

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
.home{
  display:flex;
  flex-direction:column;
  gap:1.75rem;
}

.home-top{
  display:flex;
  flex-direction:column;
  gap:1.25rem;
}

.home-middle{
  padding-top:1.25rem;
  border-top:1px solid var(--c-border);
  display:flex;
  flex-direction:column;
  gap:1rem;
}

.home-bottom{
  padding-top:1.25rem;
  border-top:1px solid var(--c-border);
  display:flex;
  flex-direction:column;
  gap:1rem;
}

.section-title{
  margin:0;
  font-size:1.1rem;
  font-weight:800;
  letter-spacing:.02em;
}

.section-subtitle{
  margin:0;
  font-size:.95rem;
  color:var(--c-muted);
}

.hero{
  border-radius:var(--radius);
  padding:2.5rem 2rem;
  margin-bottom:1rem;
  background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 45%,#0ea5e9 100%);
  color:#fff;
  box-shadow:var(--shadow);
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1.5rem;
  flex-wrap:wrap;
}

.hero-main{
  flex:1 1 320px;
}

.hero-overline{
  margin:0 0 .35rem 0;
  font-size:.8rem;
  letter-spacing:.16em;
  text-transform:uppercase;
  opacity:.85;
}

.hero-panel{
  flex:0 0 auto;
  display:flex;
  flex-direction:column;
  gap:.35rem;
  padding:.8rem .95rem;
  border-radius:.9rem;
  background:rgba(15,23,42,.16);
  border:1px solid rgba(15,23,42,.25);
  min-width:210px;
}

.hero-metric{
  display:flex;
  align-items:baseline;
  justify-content:space-between;
  gap:.75rem;
}

.hero-metric-label{
  font-size:.8rem;
  text-transform:uppercase;
  letter-spacing:.12em;
  opacity:.9;
}

.hero-metric-value{
  font-weight:800;
  font-size:1.4rem;
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
  .hero{flex-direction:column;align-items:flex-start;}
  .hero-panel{width:100%;}
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

.middle-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(260px,1fr));
  gap:.9rem;
}

.middle-card{
  text-decoration:none;
  color:inherit;
  display:flex;
  flex-direction:column;
  gap:.5rem;
  transition:transform .06s ease, box-shadow .06s ease;
}

.middle-card:hover{
  transform:translateY(-1px);
  box-shadow:0 8px 20px rgba(15,23,42,.12);
}

.middle-title{
  margin:0;
  font-weight:800;
  color:var(--c-text);
}

.middle-text{
  margin:0;
  font-size:.95rem;
  color:var(--c-muted);
}

.middle-meta{
  margin-top:.25rem;
  display:flex;
  align-items:baseline;
  gap:.35rem;
}

.middle-count{
  font-weight:800;
  font-size:1.2rem;
}

.middle-label{
  font-size:.85rem;
  color:var(--c-muted);
}

.map-preview{
  display:flex;
  justify-content:space-between;
  gap:1.25rem;
  align-items:flex-start;
}

.map-preview-main{
  flex:1 1 auto;
}

.map-text{
  margin:.25rem 0 1rem 0;
  font-size:.96rem;
  color:var(--c-muted);
}

.btn-map{
  margin-top:.25rem;
}

.map-preview-legend{
  flex:0 0 220px;
  border-radius:.75rem;
  border:1px dashed var(--c-border);
  padding:.75rem .9rem;
  background:#f9fafb;
}

.map-legend-row{
  display:flex;
  align-items:center;
  gap:.5rem;
  font-size:.88rem;
  color:#4b5563;
  margin-bottom:.35rem;
}

.map-legend-row:last-child{
  margin-bottom:0;
}

.map-swatch{
  width:14px;
  height:14px;
  border-radius:3px;
  border:1px solid rgba(0,0,0,.2);
}

.map-swatch-wc{background-color:rgba(0,150,255,.3);}
.map-swatch-dept{background-color:rgba(0,200,120,.3);}
.map-swatch-other{background-color:rgba(180,180,180,.3);}

.home-footer{
  margin-top:.5rem;
}

@media (max-width:1200px){
  .kpis{grid-template-columns:repeat(2,minmax(240px,1fr));}
  .feature-grid{grid-template-columns:repeat(2,minmax(240px,1fr));}
  .middle-grid{grid-template-columns:repeat(2,minmax(240px,1fr));}
}

@media (max-width:800px){
  .kpis{grid-template-columns:1fr;}
  .feature-grid{grid-template-columns:1fr;}
  .middle-grid{grid-template-columns:1fr;}
  .map-preview{flex-direction:column;}
  .map-preview-legend{width:100%;}
}
</style>