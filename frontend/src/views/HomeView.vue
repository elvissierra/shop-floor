<template>
  <section class="home">
    <PageHeader title="Dashboard" subtitle="Overview" />
    <div class="kpis">
      <div class="kpi">
        <div class="kpi-num">{{ deptCount }}</div>
        <div class="kpi-label">Departments</div>
      </div>
      <div class="kpi">
        <div class="kpi-num">{{ partCount }}</div>
        <div class="kpi-label">Parts</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useShopFloorStore } from '../stores/shopFloor'
import PageHeader from '../components/PageHeader.vue'

const store = useShopFloorStore()
onMounted(() => { if (!store.shopFloorData) store.fetchShopFloorData() })
const deptCount = computed(() => store.shopFloorData?.departments?.length ?? 0)
const partCount = computed(() => store.shopFloorData?.parts?.length ?? 0)
</script>

<style scoped>
.kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: .75rem;
}
.kpi {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  padding: 1rem;
  box-shadow: var(--shadow);
}
.kpi-num { font-size: 1.75rem; font-weight: 800; color: var(--c-text); line-height: 1.2; }
.kpi-label { margin-top: .2rem; color: var(--c-muted); font-size: .95rem; }
.kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: .75rem;
}
.kpi {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  padding: 1rem;
  box-shadow: var(--shadow);
}
.kpi-num { font-size: 1.75rem; font-weight: 800; color: var(--c-text); line-height: 1.2; }
.kpi-label { margin-top: .2rem; color: var(--c-muted); font-size: .95rem; }
</style>