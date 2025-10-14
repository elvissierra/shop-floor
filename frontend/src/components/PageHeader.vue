<template>
  <header class="page-header" :aria-label="ariaLabel">
    <div class="titles">
      <h1 class="title">{{ title }}</h1>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
    <div class="actions">
      <slot name="actions" />
    </div>
  </header>
</template>

<script setup>
const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  ariaLabel: { type: String, default: 'Section header' },
})
</script>

<style scoped>
.page-header { display:flex; align-items:flex-end; justify-content:space-between; gap:1rem; margin:.25rem 0 1rem; }
.titles { display:flex; flex-direction:column; gap:.25rem; }
.title { margin:0; font-size:1.5rem; line-height:1.2; }
.subtitle { margin:0; color:var(--c-muted); font-size:.95rem; }
.actions { display:flex; align-items:center; gap:.5rem; }
</style>