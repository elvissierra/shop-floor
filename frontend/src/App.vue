<template>
  <div class="app">
    <nav class="navbar" role="navigation" aria-label="Main">
      <div class="nav-inner container">
        <router-link to="/shopfloor" class="brand">Shop Floor</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Dashboard</router-link>
          <router-link to="/shopfloor" class="nav-link">Shop Floor</router-link>
          <router-link to="/departments" class="nav-link">Departments</router-link>
          <router-link to="/work-centers" class="nav-link">Work Centers</router-link>
          <router-link to="/parts" class="nav-link">Parts</router-link>
        </div>
      </div>
    </nav>
    <a href="#main" class="skip">Skip to content</a>
    <main id="main" class="main-content">
      <div class="container">
        <Breadcrumbs />
        
        <router-view />
      </div>
    </main>
    <Toast />
  </div>
</template>

<script setup>
import Toast from './components/Toast.vue'
import Breadcrumbs from './components/Breadcrumbs.vue'
</script>

<style>
  .app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: var(--c-bg);
    min-width: 1024px;
    overflow-x: auto;
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

.nav-link.router-link-exact-active {
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

/* ensure wide desktop feel and avoid accidental shrinkage by nested views */

.skip{position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden}
.skip:focus{position:static;width:auto;height:auto;padding:.25rem .5rem;background:#fff;border:1px solid var(--c-border);border-radius:6px;margin:.25rem 1rem}

.nav-inner{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1rem;
  margin:0 auto;
}
</style>
