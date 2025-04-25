<template>
  <div class="app">
    <nav class="navbar">
      <router-link to="/" class="nav-link">Shop Floor Dashboard</router-link>
    </nav>
    
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #2c3e50;
  padding: 1rem 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
}

.nav-link:hover {
  color: #42b983;
}

.main-content {
  flex: 1;
  background-color: #f5f5f5;
}
</style>
