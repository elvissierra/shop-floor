<template>
  <div class="app">
    <nav class="navbar" role="navigation" aria-label="Main">
      <router-link to="/" class="brand">Shop Floor</router-link>
      <div class="nav-links">
        <router-link to="/" class="nav-link" exact>Dashboard</router-link>
        <router-link to="/departments" class="nav-link">Departments</router-link>
        <router-link to="/parts" class="nav-link">Parts</router-link>
      </div>
    </nav>
    <main class="main-content">
      <div class="container">
        <section v-if="isHome" class="dash-strip" aria-label="Dashboard summary">
          <div class="dash-card">
            <div class="dash-kpi">{{ deptCount }}</div>
            <div class="dash-label">Departments</div>
          </div>
          <div class="dash-card">
            <div class="dash-kpi">{{ partCount }}</div>
            <div class="dash-label">Parts</div>
          </div>
        </section>
        <router-view />
      </div>
    </main>
    <Toast />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useShopFloorStore } from './stores/shopFloor'
import Toast from './components/Toast.vue'

const route = useRoute()
const isHome = computed(() => route.path === '/')
const store = useShopFloorStore()
const deptCount = computed(() => store.shopFloorData?.departments?.length ?? 0)
const partCount = computed(() => store.shopFloorData?.parts?.length ?? 0)
</script>

<style>
  .app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #f6f7f9;
    min-width: 1024px;
  }

.container {
  width: min(1280px, 92vw);
  margin: 0 auto;
}

.navbar {
  background-color: #111827;
  padding: .75rem 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: sticky;
  top: 0;
  z-index: 40;
}

.brand {
  color: #fff;
  text-decoration: none;
  font-weight: 800;
  letter-spacing: .2px;
}

.nav-links {
  display: flex;
  gap: .75rem;
}

.nav-link {
  color: #e5e7eb;
  text-decoration: none;
  font-size: .95rem;
  padding: .35rem .6rem;
  border-radius: .5rem;
}

.nav-link.router-link-active {
  background: #1f2937;
  color: #fff;
}

.nav-link:hover {
  color: #fff;
}

.main-content {
  flex: 1;
  padding: 1rem;
}
</style>
