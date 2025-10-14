<template>
  <section class="sf">
    <PageHeader title="Shop Floor" subtitle="Operations" />
    <router-view />
  </section>
</template>

<script setup>
import PageHeader from '../components/PageHeader.vue'
</script>

<style scoped>
.sf { padding: 0 1rem 1rem; }
</style>