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
      <router-view />
    </main>
    <Toast />
  </div>
</template>

<script setup>
import Toast from './components/Toast.vue'
</script>

<style>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f6f7f9;
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
