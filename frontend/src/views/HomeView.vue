<template>
  <section class="home">
    <div class="hero" role="banner" aria-label="Shop Floor hero">
      <h1 class="hero-title">Dashboard</h1>
      <p class="hero-sub">
        Insights leading dashboard.
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
        <div class="kpi-num">{{ partCount }}</div>
        <div class="kpi-label">Parts</div>
      </div>
    </div>

    <div class="feature-grid">
      <div class="card feature">
        <h3 class="feature-title">Fast CRUD</h3>
        <p class="feature-text">Create, update, and search Departments and Parts with an optimistic UI and toasts.</p>
      </div>
      <div class="card feature">
        <h3 class="feature-title">GraphQL Driven</h3>
        <p class="feature-text">Typed queries with camelCase fields, pagination, and clear errors for easy debugging.</p>
      </div>
      <div class="card feature">
        <h3 class="feature-title">Desktop-First UX</h3>
        <p class="feature-text">Full-width layout, clean spacing, and accessible controls tuned for large screens.</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useShopFloorStore } from '../stores/shopFloor'


const store = useShopFloorStore()
onMounted(() => { if (!store.shopFloorData) store.fetchShopFloorData() })
const deptCount = computed(() => store.shopFloorData?.departments?.length ?? 0)
const partCount = computed(() => store.shopFloorData?.parts?.length ?? 0)
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

.kpis{display:grid;grid-template-columns:repeat(2,minmax(280px,1fr));gap:.9rem;margin:1rem 0 1.25rem 0;}
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
</style>