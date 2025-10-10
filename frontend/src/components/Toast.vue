<template>
  <div class="toast-wrap" role="status" aria-live="polite">
    <transition-group name="toast" tag="div">
      <div v-for="t in toasts" :key="t.id" class="toast" :class="t.type"
           @mouseenter="pause(t.id)" @mouseleave="resume(t.id)">
        <strong class="title">{{ t.title }}</strong>
        <div class="msg">{{ t.message }}</div>
        <button class="close" aria-label="Dismiss" @click="dismiss(t.id)">×</button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const toasts = ref([])
let unsub

function show(payload) {
  const id = Math.random().toString(36).slice(2)
  const ttl = payload.ttl ?? 3500
  const toast = {
    id,
    type: payload.type || 'info',
    title: payload.title || '',
    message: payload.message || '',
    ttl,
    paused: false,
    started: Date.now(),
    remaining: ttl,
  }
  toasts.value.push(toast)
  toast._timer = setTimeout(() => dismiss(id), ttl)
}

function dismiss(id) {
  const i = toasts.value.findIndex(t => t.id === id)
  if (i !== -1) {
    clearTimeout(toasts.value[i]._timer)
    toasts.value.splice(i, 1)
  }
}

function pause(id) {
  const t = toasts.value.find(t => t.id === id)
  if (!t || t.paused) return
  t.paused = true
  clearTimeout(t._timer)
  t.remaining = Math.max(0, t.ttl - (Date.now() - t.started))
}

function resume(id) {
  const t = toasts.value.find(t => t.id === id)
  if (!t || !t.paused) return
  t.paused = false
  t.started = Date.now()
  t._timer = setTimeout(() => dismiss(id), t.remaining)
}

// tiny event bus
function subscribe(cb) {
  window.addEventListener('shopfloor:toast', cb)
  return () => window.removeEventListener('shopfloor:toast', cb)
}

onMounted(() => { unsub = subscribe((e) => show(e.detail)) })
onUnmounted(() => { if (unsub) unsub() })
</script>

<style scoped>
.toast-wrap { position: fixed; right: 16px; bottom: 16px; z-index: 9999; pointer-events: none; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(10px); }
.toast-enter-active, .toast-leave-active { transition: all .18s ease; }
.toast { pointer-events: auto; background: #1f2937; color: #fff; border-radius: 8px; padding: .75rem .875rem; margin-top: .5rem; min-width: 260px; max-width: 360px; box-shadow: 0 6px 18px rgba(0,0,0,.18); position: relative; }
.toast.success { background: #166534; }
.toast.error { background: #7f1d1d; }
.toast.info { background: #1f2937; }
.toast .title { font-weight: 700; display: block; margin-bottom: .125rem; }
.toast .msg { opacity: .95; }
.toast .close { position: absolute; top: 6px; right: 8px; background: transparent; border: none; color: #fff; font-size: 18px; cursor: pointer; }
</style>