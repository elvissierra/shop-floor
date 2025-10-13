<template>
  <form @submit.prevent="onSubmit" class="form" aria-describedby="form-help">
    <div class="field">
      <label for="title">Title <span class="req">*</span></label>
      <input
        id="title"
        v-model.trim="local.title"
        type="text"
        required
        :maxlength="50"
        :disabled="submitting"
        autocomplete="off"
        autofocus
        aria-invalid="errors.title ? 'true' : 'false'"
        aria-describedby="title-help"
      />
      <small id="title-help" class="hint">Department name (max 50 chars).</small>
      <p v-if="errors.title" class="err">{{ errors.title }}</p>
    </div>

    <div class="field">
      <label for="desc">Description</label>
      <textarea
        id="desc"
        v-model.trim="local.description"
        rows="3"
        :maxlength="255"
        :disabled="submitting"
        aria-describedby="desc-help"
      ></textarea>
      <small id="desc-help" class="hint">Optional. Max 255 characters.</small>
    </div>

    <div class="actions">
      <button type="button" class="btn" @click="$emit('cancel')" :disabled="submitting">Cancel</button>
      <button type="submit" class="btn primary" :disabled="submitting || !!errors.title">
        <span v-if="submitting">Saving…</span>
        <span v-else>Save</span>
      </button>
    </div>
    <p id="form-help" class="sr">Fields marked with * are required.</p>
  </form>
</template>

<script setup>
import { reactive, watch, computed } from 'vue'

const props = defineProps({
  modelValue: { type: Object, default: () => ({ title: '', description: '' }) },
  submitting: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])

const local = reactive({ title: '', description: '' })
const errors = reactive({ title: '' })

watch(() => props.modelValue, (v) => {
  local.title = v?.title ?? ''
  local.description = v?.description ?? ''
  validate()
}, { immediate: true })

watch(local, (v) => {
  emit('update:modelValue', { ...v })
  validate()
}, { deep: true })

function validate() {
  errors.title = ''
  if (!local.title) {
    errors.title = 'Title is required.'
  } else if (local.title.length > 50) {
    errors.title = 'Title must be 50 characters or fewer.'
  }
}

function onSubmit() {
  validate()
  if (errors.title) return
  emit('submit')
}
</script>

<style scoped>
.form { display:flex; flex-direction:column; gap:.75rem; }
.field { display:flex; flex-direction:column; gap:.25rem; }
label { font-weight:600; color:#111827; }
.req { color:#dc2626; }
input, textarea { border:1px solid #d1d5db; border-radius:8px; padding:.5rem .6rem; font-size: 14px; background:#fff; }
input:focus, textarea:focus { outline: none; border-color:#2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.15); }
.hint { color:#6b7280; font-size:12px; }
.err { color:#b91c1c; font-size: 13px; margin:0; }
.actions { display:flex; justify-content:flex-end; gap:.5rem; margin-top:.5rem; }
.btn { border:none; border-radius:8px; padding:.5rem .9rem; cursor:pointer; background:#e5e7eb; }
.btn.primary { background:#2563eb; color:#fff; }
.btn:disabled { opacity:.6; cursor:not-allowed; }
.sr { position:absolute; left:-10000px; width:1px; height:1px; overflow:hidden; }
</style>