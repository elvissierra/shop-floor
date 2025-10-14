<template>
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <ol>
      <li v-for="(bc, i) in items" :key="i">
        <router-link v-if="bc.to" :to="bc.to">{{ bc.label }}</router-link>
        <span v-else aria-current="page">{{ bc.label }}</span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const items = computed(() => {
  const base = [{ label: 'Home', to: '/' }]
  const crumbs = route.meta?.breadcrumb || []
  return [...base, ...crumbs]
})
</script>

<style scoped>
.breadcrumbs { font-size:.9rem; color:var(--c-muted); margin:.25rem 0 .5rem; }
.breadcrumbs ol { display:flex; gap:.35rem; list-style:none; padding:0; margin:0; flex-wrap:wrap; }
.breadcrumbs li { display:flex; align-items:center; gap:.35rem; }
.breadcrumbs li::after { content:'/'; opacity:.6; }
.breadcrumbs li:last-child::after { content:''; }
.breadcrumbs a { color:inherit; text-decoration:none; }
.breadcrumbs a:hover { text-decoration:underline; }
</style>