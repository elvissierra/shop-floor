<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-link" @click="goBack">← Back</button>

        <div v-if="part">
          <h1>{{ part.name }}</h1>
          <p class="subtitle">
            <template v-if="departmentName">
              Department: <strong>{{ departmentName }}</strong>
            </template>
            <template v-else-if="part.departmentId != null">
              Department ID: <strong>{{ part.departmentId }}</strong>
            </template>
            <template v-else>
              <span class="muted">No department assigned.</span>
            </template>
          </p>
        </div>
      </div>
    </header>

    <div v-if="errorMessage" class="status status-error">
      {{ errorMessage }}
    </div>

    <section class="grid">
      <div class="card">
        <h2>Work Orders for this Part</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!workOrdersForPart.length">
          <p class="muted">No work orders reference this part.</p>
        </div>
        <ul v-else class="list">
          <li v-for="wo in workOrdersForPart" :key="wo.id">
            <div class="row-main">
              <span class="wo-number">WO {{ wo.number }}</span>
              <span class="wo-status">{{ wo.status }}</span>
            </div>
            <div class="row-sub">
              Qty: {{ wo.quantity }}
              <span v-if="wo.workCenterId">
                • Work Center
                <button class="link-chip" @click="goToWorkCenter(wo.workCenterId)">
                  #{{ wo.workCenterId }} {{ workCenterName(wo.workCenterId) }}
                </button>
              </span>
            </div>
          </li>
        </ul>
      </div>

      <div class="card">
        <h2>Routings</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!routingsForPart.length">
          <p class="muted">No routings defined for this part.</p>
        </div>
        <ul v-else class="list">
          <li v-for="routing in routingsForPart" :key="routing.id">
            <div class="row-main">
              {{ routing.name }}
              <span v-if="routing.version" class="tag">
                v{{ routing.version }}
              </span>
            </div>
            <div class="row-sub">
              Steps:
              {{ stepsByRouting[routing.id]?.length ?? 0 }}
            </div>
          </li>
        </ul>
      </div>

      <div class="card card-wide">
        <h2>Bills of Material</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!bomsForPart.length">
          <p class="muted">No BOMs are defined for this part.</p>
        </div>
        <ul v-else class="list">
          <li v-for="bom in bomsForPart" :key="bom.id">
            <div class="row-main">
              BOM #{{ bom.id }}
              <span v-if="bom.revision" class="tag">
                Rev {{ bom.revision }}
              </span>
            </div>
            <div class="row-sub">
              Components:
              {{ bomItemsByBom[bom.id]?.length ?? 0 }}
            </div>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchGraphQL } from "@/services/graphql";

type Part = {
  id: number;
  name: string;
  departmentId: number | null;
};

type Department = {
  id: number;
  title: string;
};

type WorkOrder = {
  id: number;
  number: string;
  status: string;
  quantity: number;
  partId: number;
  workCenterId: number | null;
};

type WorkCenter = {
  id: number;
  name: string;
};

type Routing = {
  id: number;
  name: string;
  partId: number;
  version: string | null;
};

type RoutingStep = {
  id: number;
  routingId: number;
  sequence: number;
  workCenterId: number | null;
  description: string | null;
  standardMinutes: number | null;
};

type BOM = {
  id: number;
  partId: number;
  revision: string | null;
};

type BOMItem = {
  id: number;
  bomId: number;
  componentPartId: number;
  quantity: number;
};

const route = useRoute();
const router = useRouter();
const idParam = route.params.id;
const partId = Number(idParam);

const loading = ref(false);
const errorMessage = ref<string | null>(null);

const part = ref<Part | null>(null);
const departments = ref<Department[]>([]);
const workOrders = ref<WorkOrder[]>([]);
const workCenters = ref<WorkCenter[]>([]);
const routings = ref<Routing[]>([]);
const routingSteps = ref<RoutingStep[]>([]);
const boms = ref<BOM[]>([]);
const bomItems = ref<BOMItem[]>([]);

const departmentName = computed(() => {
  const current = part.value;
  if (!current || current.departmentId == null) return null;
  const dept = departments.value.find((d) => d.id === current.departmentId);
  return dept ? dept.title : null;
});

const workOrdersForPart = computed(() =>
  workOrders.value.filter((wo) => wo.partId === partId)
);

const routingsForPart = computed(() =>
  routings.value.filter((r) => r.partId === partId)
);

const bomsForPart = computed(() =>
  boms.value.filter((b) => b.partId === partId)
);

const stepsByRouting = computed<Record<number, RoutingStep[]>>(() => {
  const map: Record<number, RoutingStep[]> = {};
  for (const step of routingSteps.value) {
    if (!map[step.routingId]) map[step.routingId] = [];
    map[step.routingId].push(step);
  }
  return map;
});

const bomItemsByBom = computed<Record<number, BOMItem[]>>(() => {
  const map: Record<number, BOMItem[]> = {};
  for (const item of bomItems.value) {
    if (!map[item.bomId]) map[item.bomId] = [];
    map[item.bomId].push(item);
  }
  return map;
});

function goBack() {
  router.push({ name: "parts" });
}

function goToWorkCenter(id: number) {
  router.push({ name: "work-center-detail", params: { id } });
}

function workCenterName(id: number): string {
  const wc = workCenters.value.find((w) => w.id === id);
  return wc ? wc.name : "";
}

async function loadData() {
  loading.value = true;
  errorMessage.value = null;

  const query = `
    query PartDetail($id: Int!) {
      part(id: $id) {
        id
        name
        departmentId
      }
      departments {
        id
        title
      }
      workCenters {
        id
        name
      }
      workOrders {
        id
        number
        status
        quantity
        partId
        workCenterId
      }
      routings {
        id
        name
        partId
        version
      }
      routingSteps {
        id
        routingId
        sequence
        workCenterId
        description
        standardMinutes
      }
      boms {
        id
        partId
        revision
      }
      bomItems {
        id
        bomId
        componentPartId
        quantity
      }
    }
  `;

  try {
    type Response = {
      part: Part | null;
      departments: Department[];
      workCenters: WorkCenter[];
      workOrders: WorkOrder[];
      routings: Routing[];
      routingSteps: RoutingStep[];
      boms: BOM[];
      bomItems: BOMItem[];
    };

    const data = await fetchGraphQL<Response>(query, { id: partId });

    part.value = data.part ?? null;
    departments.value = data.departments ?? [];
    workCenters.value = data.workCenters ?? [];
    workOrders.value = data.workOrders ?? [];
    routings.value = data.routings ?? [];
    routingSteps.value = data.routingSteps ?? [];
    boms.value = data.boms ?? [];
    bomItems.value = data.bomItems ?? [];

    if (!part.value) {
      errorMessage.value = `Part ${partId} not found`;
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
  gap: 1rem;
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

.subtitle {
  margin-top: 0.25rem;
  color: #444;
  font-size: 0.9rem;
}

.muted {
  color: #777;
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

.status {
  margin-top: 0.5rem;
  color: #555;
}

.status-error {
  color: #b00020;
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
  display: flex;
  gap: 0.5rem;
  align-items: center;
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

.tag {
  font-size: 0.75rem;
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
</style>