<template>
  <div class="modal-overlay" @click.self="emit('cancel')">
    <div class="modal">
      <header class="modal-header">
        <slot name="title">Dialog</slot>
        <button class="close" aria-label="Close" @click="emit('cancel')">×</button>
      </header>
      <section class="modal-body">
        <slot />
      </section>
      <footer class="modal-footer">
        <slot name="footer"></slot>
      </footer>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['cancel'])
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.45); display:flex; align-items:center; justify-content:center; z-index: 50; }
.modal { width: min(560px, 92vw); background: #fff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,.25); overflow:hidden; }
.modal-header { display:flex; align-items:center; justify-content:space-between; padding: .9rem 1rem; border-bottom: 1px solid #eee; font-weight: 700; }
.modal-body { padding: 1rem; }
.modal-footer { padding: .75rem 1rem; border-top: 1px solid #eee; display:flex; gap:.5rem; justify-content:flex-end; }
.close { appearance:none; border:none; background:transparent; font-size: 22px; cursor:pointer; line-height:1; }
</style>