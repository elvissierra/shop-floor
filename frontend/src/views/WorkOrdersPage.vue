<template>
  <div class="page">
    <header class="page-header">
      <div>
        <h1>Work Orders</h1>
        <p class="subtitle">{{ orders.length }} total</p>
      </div>
      <button class="btn-primary" @click="openCreate">+ Add Work Order</button>
    </header>

    <section class="content">
      <div v-if="loading" class="status">Loading work orders…</div>
      <div v-else-if="errorMessage" class="status status-error">{{ errorMessage }}</div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Number</th>
            <th>Status</th>
            <th>Qty</th>
            <th>Part</th>
            <th>Department</th>
            <th>Work Center</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wo in orders" :key="wo.id" @click="goToDetail(wo.id)" class="row-clickable">
            <td>{{ wo.id }}</td>
            <td>{{ wo.number }}</td>
            <td><span class="badge" :class="`badge-${wo.status}`">{{ wo.status }}</span></td>
            <td>{{ wo.quantity }}</td>
            <td>{{ partName(wo.partId) || (wo.partId ? `#${wo.partId}` : '—') }}</td>
            <td>{{ departmentName(wo.departmentId) || (wo.departmentId ? `#${wo.departmentId}` : '—') }}</td>
            <td>{{ workCenterName(wo.workCenterId) || (wo.workCenterId ? `#${wo.workCenterId}` : '—') }}</td>
          </tr>
          <tr v-if="!orders.length">
            <td colspan="7" class="empty-row">No work orders yet. Use "+ Add Work Order" to create one.</td>
          </tr>
        </tbody>
      </table>
    </section>

    <Modal v-if="showModal" @cancel="closeModal">
      <template #title>{{ editing ? 'Edit Work Order' : 'New Work Order' }}</template>
      <form class="form" @submit.prevent="saveOrder">
        <div class="field">
          <label for="wo-number">Number <span class="req">*</span></label>
          <input id="wo-number" v-model.trim="form.number" type="text" required :disabled="submitting" autocomplete="off" />
        </div>
        <div class="field">
          <label for="wo-status">Status</label>
          <select id="wo-status" v-model="form.status" :disabled="submitting">
            <option value="open">open</option>
            <option value="in_progress">in_progress</option>
            <option value="complete">complete</option>
            <option value="cancelled">cancelled</option>
          </select>
        </div>
        <div class="field">
          <label for="wo-qty">Quantity</label>
          <input id="wo-qty" v-model.number="form.quantity" type="number" min="1" :disabled="submitting" />
        </div>
        <div class="field">
          <label for="wo-part">Part <span class="req">*</span></label>
          <select id="wo-part" v-model.number="form.partId" :disabled="submitting">
            <option :value="null" disabled>Select a part</option>
            <option v-for="p in parts" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="field">
          <label for="wo-dept">Department</label>
          <select id="wo-dept" v-model.number="form.departmentId" :disabled="submitting">
            <option :value="null">Unassigned</option>
            <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.title }}</option>
          </select>
        </div>
        <div class="field">
          <label for="wo-wc">Work Center</label>
          <select id="wo-wc" v-model.number="form.workCenterId" :disabled="submitting">
            <option :value="null">Unassigned</option>
            <option v-for="wc in workCenters" :key="wc.id" :value="wc.id">{{ wc.name }}</option>
          </select>
        </div>
        <div class="actions">
          <button type="button" class="btn" @click="closeModal" :disabled="submitting">Cancel</button>
          <button type="submit" class="btn primary" :disabled="submitting || !form.number || !form.partId">
            <span v-if="submitting">Saving…</span>
            <span v-else>Save</span>
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchGraphQL } from '@/services/graphql'
import Modal from '@/components/Modal.vue'
import { useToast } from '../composables/useToast'

type WorkOrder = {
  id: number
  number: string
  status: string
  quantity: number
  partId: number | null
  departmentId: number | null
  workCenterId: number | null
}

type Part = { id: number; name: string }
type Department = { id: number; title: string }
type WorkCenter = { id: number; name: string }

const router = useRouter()
const { push: toast } = useToast()

const orders = ref<WorkOrder[]>([])
const parts = ref<Part[]>([])
const departments = ref<Department[]>([])
const workCenters = ref<WorkCenter[]>([])
const loading = ref(false)
const errorMessage = ref<string | null>(null)

const showModal = ref(false)
const editing = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)

type OrderForm = {
  number: string
  status: string
  quantity: number
  partId: number | null
  departmentId: number | null
  workCenterId: number | null
}

const form = ref<OrderForm>({
  number: '', status: 'open', quantity: 1, partId: null, departmentId: null, workCenterId: null,
})

const partName = (id: number | null) => parts.value.find(p => p.id === id)?.name ?? null
const departmentName = (id: number | null) => departments.value.find(d => d.id === id)?.title ?? null
const workCenterName = (id: number | null) => workCenters.value.find(wc => wc.id === id)?.name ?? null

function openCreate() {
  editing.value = false
  editingId.value = null
  form.value = { number: '', status: 'open', quantity: 1, partId: null, departmentId: null, workCenterId: null }
  showModal.value = true
}

function closeModal() { showModal.value = false }

async function saveOrder() {
  submitting.value = true
  try {
    if (editing.value && editingId.value != null) {
      const mutation = `
        mutation UpdateWorkOrder($id: Int!, $data: WorkOrderInput!) {
          updateWorkOrder(id: $id, data: $data) { id number status quantity partId departmentId workCenterId }
        }
      `
      type R = { updateWorkOrder: WorkOrder }
      const data = await fetchGraphQL<R>(mutation, { id: editingId.value, data: form.value })
      const idx = orders.value.findIndex(o => o.id === editingId.value)
      if (idx !== -1) orders.value[idx] = data.updateWorkOrder
      toast({ type: 'success', title: 'Work order updated', message: data.updateWorkOrder.number })
    } else {
      const mutation = `
        mutation AddWorkOrder($data: WorkOrderInput!) {
          addWorkOrder(data: $data) { id number status quantity partId departmentId workCenterId }
        }
      `
      type R = { addWorkOrder: WorkOrder }
      const data = await fetchGraphQL<R>(mutation, { data: form.value })
      orders.value.unshift(data.addWorkOrder)
      toast({ type: 'success', title: 'Work order created', message: data.addWorkOrder.number })
    }
    closeModal()
  } catch (err: any) {
    toast({ type: 'error', title: 'Save failed', message: err?.message ?? String(err) })
  } finally {
    submitting.value = false
  }
}

function goToDetail(id: number) {
  router.push({ name: 'work-order-detail', params: { id } })
}

async function loadData() {
  loading.value = true
  errorMessage.value = null
  const query = `
    query WorkOrders {
      workOrders { id number status quantity partId departmentId workCenterId }
      parts { id name }
      departments { id title }
      workCenters { id name }
    }
  `
  try {
    type R = { workOrders: WorkOrder[]; parts: Part[]; departments: Department[]; workCenters: WorkCenter[] }
    const data = await fetchGraphQL<R>(query)
    orders.value = data.workOrders ?? []
    parts.value = data.parts ?? []
    departments.value = data.departments ?? []
    workCenters.value = data.workCenters ?? []
  } catch (err: any) {
    errorMessage.value = err?.message ?? String(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.page { padding: 1.5rem 2rem; display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-end; }
.subtitle { margin-top: 0.25rem; color: #666; font-size: 0.9rem; }
.btn-primary { background: var(--c-primary); color: #fff; border: none; border-radius: 8px; padding: 0.45rem 0.9rem; cursor: pointer; font-size: 0.9rem; }
.btn-primary:hover { opacity: 0.95; }
.content { border-radius: 8px; border: 1px solid #ddd; background: #fafafa; padding: 1rem; }
.table { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
.table th, .table td { padding: 0.5rem 0.75rem; border-bottom: 1px solid #e1e1e1; text-align: left; }
.table th { font-weight: 600; color: #444; }
.row-clickable { cursor: pointer; }
.row-clickable:hover { background-color: #f0f4ff; }
.empty-row { text-align: center; color: #888; padding: 1.5rem 0; }
.status { padding: 0.5rem; color: #555; }
.status-error { color: #b00020; }
.badge { font-size: 0.78rem; padding: 0.15rem 0.5rem; border-radius: 999px; border: 1px solid #ccc; }
.badge-open { background: #dbeafe; color: #1e40af; border-color: #bfdbfe; }
.badge-in_progress { background: #fef3c7; color: #92400e; border-color: #fde68a; }
.badge-complete { background: #d1fae5; color: #065f46; border-color: #a7f3d0; }
.badge-cancelled { background: #f3f4f6; color: #6b7280; border-color: #e5e7eb; }
.form { display: flex; flex-direction: column; gap: 0.75rem; }
.field { display: flex; flex-direction: column; gap: 0.25rem; }
.req { color: var(--c-danger-600); }
.form input, .form select { border: 1px solid var(--c-border); border-radius: 8px; padding: 0.5rem 0.6rem; background: #fff; }
.actions { display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.5rem; }
.btn { border: none; border-radius: 8px; padding: 0.5rem 0.9rem; cursor: pointer; background: #e5e7eb; }
.btn.primary { background: var(--c-primary); color: #fff; }
</style>
