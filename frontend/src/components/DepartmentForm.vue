<template>
  <form @submit.prevent="onSubmit" class="form">
    <div class="field">
      <label for="title">Title</label>
      <input id="title" v-model.trim="local.title" type="text" required :disabled="submitting" />
    </div>
    <div class="field">
      <label for="desc">Description</label>
      <textarea id="desc" v-model.trim="local.description" rows="3" :disabled="submitting"></textarea>
    </div>

    <div class="actions">
      <button type="button" class="btn" @click="$emit('cancel')" :disabled="submitting">Cancel</button>
      <button type="submit" class="btn primary" :disabled="submitting">
        <span v-if="submitting">Saving…</span>
        <span v-else>Save</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  modelValue: { type: Object, default: () => ({ title: '', description: '' }) },
  submitting: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])

const local = reactive({ title: '', description: '' })

watch(() => props.modelValue, (v) => {
  local.title = v?.title ?? ''
  local.description = v?.description ?? ''
}, { immediate: true })

watch(local, (v) => emit('update:modelValue', { ...v }), { deep: true })

function onSubmit() {
  if (!local.title) return
  emit('submit')
}
</script>

<style scoped>
.form { display:flex; flex-direction:column; gap:.75rem; }
.field { display:flex; flex-direction:column; gap:.25rem; }
label { font-weight:600; color:#2c3e50; }
input, textarea { border:1px solid #d9d9d9; border-radius:8px; padding:.5rem .6rem; font-size: 14px; }
.actions { display:flex; justify-content:flex-end; gap:.5rem; margin-top:.5rem; }
.btn { border:none; border-radius:8px; padding:.5rem .9rem; cursor:pointer; background:#e9ecef; }
.btn.primary { background:#2c3e50; color:#fff; }
.btn:disabled { opacity:.6; cursor:not-allowed; }
</style>