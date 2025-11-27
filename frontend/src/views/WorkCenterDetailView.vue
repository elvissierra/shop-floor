<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-link" @click="goBack">← Back</button>
      
        <div v-if="workCenter">
          <h1>{{ workCenter.name }}</h1>
          <p class="subtitle">
            Code: <strong>{{ workCenter.code || "—" }}</strong>
            <span class="divider">•</span>
            <template v-if="departmentName">
              Department: <strong>{{ departmentName }}</strong>
            </template>
            <template v-else>
              Department ID: <strong>{{ workCenter.departmentId ?? "—" }}</strong>
            </template>
          </p>
        </div>
      </div>
    
      <button
        v-if="workCenter"
        class="btn-primary"
        @click="goToFloorMap"
      >
        View on Floor Map
      </button>
    </header>

    <div v-if="errorMessage" class="status status-error">
      {{ errorMessage }}
    </div>

    <section class="grid">
      <div class="card">
        <div class="card-header-row">
          <h2>Work Orders at this Center</h2>
          <button
            v-if="workCenter"
            class="btn-secondary"
            @click="openOrderModal"
          >
            + Add Work Order
          </button>
        </div>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!workOrdersForCenter.length">
          <p class="muted">No work orders linked to this work center.</p>
        </div>
        <ul v-else class="list">
          <li v-for="wo in workOrdersForCenter" :key="wo.id">
            <div class="row-main">
              <span class="wo-number">{{ wo.number }}</span>
              <span class="wo-status">{{ wo.status }}</span>
            </div>
            <div class="row-sub">
                Qty: {{ wo.quantity }}
                <span v-if="wo.partId">
                  • Part
                  <button
                    class="link-chip"
                    @click.stop="goToPart(wo.partId)"
                  >
                    #{{ wo.partId }}
                  </button>
                </span>
              </div>
          </li>
        </ul>
      </div>

      <div class="card">
        <h2>Routing Steps</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!routingStepsForCenter.length">
          <p class="muted">No routing steps assigned to this work center.</p>
        </div>
        <ul v-else class="list">
          <li v-for="step in routingStepsForCenter" :key="step.id">
            <div class="row-main">
              Sequence {{ step.sequence }}
            </div>
            <div class="row-sub">
              {{ step.description || "No description" }}
              <span v-if="step.standardMinutes">
                • {{ step.standardMinutes }} min
              </span>
            </div>
          </li>
        </ul>
      </div>

      <div class="card card-wide">
        <h2>Floor Zones for this Center</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!floorZonesForCenter.length">
          <p class="muted">This work center is not referenced by any floor zones.</p>
        </div>
        <ul v-else class="list">
          <li v-for="zone in floorZonesForCenter" :key="zone.id">
            <div class="row-main">
              {{ zone.name }} (Floor {{ zone.floorId }})
            </div>
            <div class="row-sub">
              Type: {{ zone.zoneType || "—" }}
              • Polygon: {{ zone.polygon }}
            </div>
          </li>
        </ul>
      </div>
    </section>

    <Modal v-if="showOrderModal" @cancel="closeOrderModal">
      <template #title>New Work Order</template>
      <form class="form" @submit.prevent="saveOrder">
        <div class="field">
          <label for="wo-number">Number <span class="req">*</span></label>
          <input
            id="wo-number"
            v-model.trim="orderForm.number"
            type="text"
            required
            :disabled="submittingOrder"
            autocomplete="off"
          />
        </div>
        <div class="field">
          <label for="wo-qty">Quantity</label>
          <input
            id="wo-qty"
            v-model.number="orderForm.quantity"
            type="number"
            min="1"
            :disabled="submittingOrder"
          />
        </div>
        <div class="field">
          <label for="wo-part">Part <span class="req">*</span></label>
          <select
            id="wo-part"
            v-model.number="orderForm.partId"
            :disabled="submittingOrder || !parts.length"
          >
            <option v-if="!parts.length" :value="null" disabled>
              No parts available
            </option>
            <option v-for="p in parts" :key="p.id" :value="p.id">
              #{{ p.id }} — {{ p.name }}
            </option>
          </select>
        </div>
        <div class="actions">
          <button
            type="button"
            class="btn"
            @click="closeOrderModal"
            :disabled="submittingOrder"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn primary"
            :disabled="submittingOrder || !orderForm.number || !orderForm.partId"
          >
            <span v-if="submittingOrder">Saving…</span>
            <span v-else>Save</span>
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchGraphQL } from "@/services/graphql";
import Modal from "@/components/Modal.vue";
import { useToast } from "../composables/useToast";

type WorkCenter = {
  id: number;
  name: string;
  code: string | null;
  departmentId: number | null;
};

type WorkOrder = {
  id: number;
  number: string;
  status: string;
  quantity: number;
  partId: number;
  workCenterId: number | null;
};

type RoutingStep = {
  id: number;
  routingId: number;
  sequence: number;
  workCenterId: number | null;
  description: string | null;
  standardMinutes: number | null;
};

type FloorZone = {
  id: number;
  floorId: number;
  name: string;
  zoneType: string | null;
  departmentId: number | null;
  workCenterId: number | null;
  polygon: string;
};

type Part = {
  id: number;
  name: string;
};


type Department = {
  id: number;
  title: string;
  description: string;
};

const route = useRoute();
const router = useRouter();
const idParam = route.params.id;
const workCenterId = Number(idParam);

const loading = ref(false);
const errorMessage = ref<string | null>(null);

const { push: toast } = useToast();

const showOrderModal = ref(false);
const submittingOrder = ref(false);

type WorkOrderForm = {
  number: string;
  quantity: number;
  partId: number | null;
};

const orderForm = ref<WorkOrderForm>({
  number: "",
  quantity: 1,
  partId: null,
});

const workCenters = ref<WorkCenter[]>([]);
const workOrders = ref<WorkOrder[]>([]);
const routingSteps = ref<RoutingStep[]>([]);
const floorZones = ref<FloorZone[]>([]);
const departments = ref<Department[]>([]);
const parts = ref<Part[]>([]);

const workCenter = computed(() =>
  workCenters.value.find((wc) => wc.id === workCenterId) || null
);

const departmentName = computed(() => {
  const wc = workCenter.value;
  if (!wc || wc.departmentId == null) return null;
  const dept = departments.value.find((d) => d.id === wc.departmentId);
  return dept ? dept.title : null;
});

const workOrdersForCenter = computed(() =>
  workOrders.value.filter((wo) => wo.workCenterId === workCenterId)
);

const routingStepsForCenter = computed(() =>
  routingSteps.value.filter((step) => step.workCenterId === workCenterId)
);

const floorZonesForCenter = computed(() =>
  floorZones.value.filter((z) => z.workCenterId === workCenterId)
);

function goBack() {
  router.push({ name: "work-centers" });
}

function goToFloorMap() {
  if (!workCenterId) return;
  router.push({ name: "floor-map", query: { workCenterId } });
}

function goToPart(id: number) {
  router.push({ name: "part-detail", params: { id } });
}

function openOrderModal() {
  orderForm.value = {
    number: "",
    quantity: 1,
    partId: parts.value[0]?.id ?? null,
  };
  showOrderModal.value = true;
}

function closeOrderModal() {
  showOrderModal.value = false;
}

async function saveOrder() {
  try {
    submittingOrder.value = true;

    const partId = orderForm.value.partId;
    if (!partId) {
      toast({
        type: "error",
        title: "Missing part",
        message: "Select a part for this work order.",
      });
      submittingOrder.value = false;
      return;
    }

    const mutation = `
      mutation AddWorkOrder($data: WorkOrderInput!) {
        addWorkOrder(data: $data) {
          id
          number
          status
          quantity
          partId
          workCenterId
        }
      }
    `;

    const payload = {
      number: orderForm.value.number,
      status: "open",
      quantity: orderForm.value.quantity,
      partId,
      workCenterId,
      departmentId: null,
    };

    type MutationResponse = { addWorkOrder: WorkOrder };
    const data = await fetchGraphQL<MutationResponse>(mutation, {
      data: payload,
    });

    workOrders.value.unshift(data.addWorkOrder);
    toast({
      type: "success",
      title: "Work order created",
      message: data.addWorkOrder.number,
    });
    closeOrderModal();
  } catch (err: any) {
    console.error(err);
    const message = err?.message ?? String(err);
    errorMessage.value = message;
    toast({
      type: "error",
      title: "Save failed",
      message,
    });
  } finally {
    submittingOrder.value = false;
  }
}

async function loadData() {
  loading.value = true;
  errorMessage.value = null;

  const query = `
    query WorkCenterDetail {
      departments {
        id
        title
        description
      }
      parts {
        id
        name
      }
      workCenters {
        id
        name
        code
        departmentId
      }
      workOrders {
        id
        number
        status
        quantity
        partId
        workCenterId
      }
      routingSteps {
        id
        routingId
        sequence
        workCenterId
        description
        standardMinutes
      }
      floorZones {
        id
        floorId
        name
        zoneType
        departmentId
        workCenterId
        polygon
      }
    }
  `;

  try {
    type Response = {
      departments: Department[];
      parts: Part[];
      workCenters: WorkCenter[];
      workOrders: WorkOrder[];
      routingSteps: RoutingStep[];
      floorZones: FloorZone[];
    };
    const data = await fetchGraphQL<Response>(query);
    departments.value = data.departments ?? [];
    parts.value = data.parts ?? [];
    workCenters.value = data.workCenters ?? [];
    workOrders.value = data.workOrders ?? [];
    routingSteps.value = data.routingSteps ?? [];
    floorZones.value = data.floorZones ?? [];

    if (!workCenter.value) {
      errorMessage.value = `Work center ${workCenterId} not found`;
    }
  } catch (err: any) {
    console.error(err);
    errorMessage.value = err?.message ?? String(err);
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped>
.page {
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.btn-link {
  border: none;
  background: none;
  color: #1976d2;
  cursor: pointer;
  padding: 0;
}

.btn-link:hover {
  text-decoration: underline;
}

.btn-primary {
  padding: 0.4rem 0.9rem;
  border-radius: 4px;
  border: none;
  background-color: #1976d2;
  color: #fff;
  font-size: 0.9rem;
  cursor: pointer;
  white-space: nowrap;
}

.btn-primary:hover {
  background-color: #115293;
}

.subtitle {
  margin-top: 0.25rem;
  color: #666;
  font-size: 0.9rem;
}

.grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1.2fr);
  grid-auto-rows: minmax(0, auto);
  gap: 1rem;
}

.card {
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #fafafa;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-wide {
  grid-column: 1 / -1;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary {
  border: none;
  border-radius: 8px;
  padding: 0.35rem 0.8rem;
  cursor: pointer;
  background: #e5e7eb;
  font-size: 0.85rem;
}

.btn-secondary:hover {
  background: #d4d4d8;
}

.status {
  color: #555;
}

.muted {
  color: #777;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.list li {
  padding: 0.4rem 0;
  border-bottom: 1px solid #e4e4e4;
}

.row-main {
  font-weight: 500;
}

.row-sub {
  font-size: 0.85rem;
  color: #666;
}

.wo-number {
  margin-right: 0.5rem;
}

.wo-status {
  font-size: 0.8rem;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
  border: 1px solid #ccc;
}

.link-chip {
  border: none;
  background: none;
  color: #1976d2;
  padding: 0;
  font-size: 0.85rem;
  cursor: pointer;
}

.link-chip:hover {
  text-decoration: underline;
}

.status {
  margin-top: 0.5rem;
  color: #555;
}

.status-error {
  color: #b00020;
}
</style>
<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.req {
  color: var(--c-danger-600);
}

.form input,
.form select {
  border: 1px solid var(--c-border);
  border-radius: 8px;
  padding: 0.5rem 0.6rem;
  background: #fff;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.btn {
  border: none;
  border-radius: 8px;
  padding: 0.5rem 0.9rem;
  cursor: pointer;
  background: #e5e7eb;
}

.btn.primary {
  background: var(--c-primary);
  color: #fff;
}
</style>