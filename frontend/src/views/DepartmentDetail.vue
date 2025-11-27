<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-link" @click="goBack">← Back</button>

        <div v-if="department">
          <h1>{{ department.title }}</h1>
          <p class="subtitle">
            <span v-if="department.description">
              {{ department.description }}
            </span>
            <span v-else class="muted">
              No description provided.
            </span>
          </p>
        </div>
      </div>

      <div class="header-stats" v-if="department">
        <div class="stat">
          <div class="stat-label">Work Centers</div>
          <div class="stat-value">{{ workCentersForDepartment.length }}</div>
        </div>
        <div class="stat">
          <div class="stat-label">Parts</div>
          <div class="stat-value">{{ partsForDepartment.length }}</div>
        </div>
        <div class="stat">
          <div class="stat-label">Floor Zones</div>
          <div class="stat-value">{{ floorZonesForDepartment.length }}</div>
        </div>
      </div>
    </header>

    <div v-if="errorMessage" class="status status-error">
      {{ errorMessage }}
    </div>

    <section class="grid">
      <div class="card">
        <h2>Work Centers in this Department</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!workCentersForDepartment.length">
          <p class="muted">No work centers are assigned to this department.</p>
        </div>
        <ul v-else class="list">
          <li
            v-for="wc in workCentersForDepartment"
            :key="wc.id"
            class="row-clickable"
            @click="goToWorkCenter(wc.id)"
          >
            <div class="row-main">
              {{ wc.name }}
              <span v-if="wc.code" class="tag">Code: {{ wc.code }}</span>
            </div>
            <div class="row-sub">
              ID: {{ wc.id }}
            </div>
          </li>
        </ul>
      </div>

      <div class="card">
        <h2>Parts in this Department</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!partsForDepartment.length">
          <p class="muted">No parts are assigned to this department.</p>
        </div>
        <ul v-else class="list">
          <li
            v-for="part in partsForDepartment"
            :key="part.id"
            class="row-clickable"
            @click="goToPart(part.id)"
          >
            <div class="row-main">
              {{ part.name }}
            </div>
            <div class="row-sub">
              Part ID: {{ part.id }}
            </div>
          </li>
        </ul>
      </div>

      <div class="card card-wide">
        <h2>Floor Zones for this Department</h2>
        <div v-if="loading" class="status">Loading…</div>
        <div v-else-if="!floorZonesForDepartment.length">
          <p class="muted">
            This department is not referenced by any floor zones.
          </p>
        </div>
        <ul v-else class="list">
          <li v-for="zone in floorZonesForDepartment" :key="zone.id">
            <div class="row-main">
              {{ zone.name }}
              <span v-if="zone.workCenterId" class="tag">
                Work Center ID: {{ zone.workCenterId }}
              </span>
            </div>
            <div class="row-sub">
              Floor {{ zone.floorId }} • Type:
              {{ zone.zoneType || "—" }}
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

type Department = {
  id: number;
  title: string;
  description: string | null;
};

type WorkCenter = {
  id: number;
  name: string;
  code: string | null;
  departmentId: number | null;
};

type Part = {
  id: number;
  name: string;
  departmentId: number;
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

const route = useRoute();
const router = useRouter();
const idParam = route.params.id;
const departmentId = Number(idParam);

const loading = ref(false);
const errorMessage = ref<string | null>(null);

const department = ref<Department | null>(null);
const workCenters = ref<WorkCenter[]>([]);
const parts = ref<Part[]>([]);
const floorZones = ref<FloorZone[]>([]);

const workCentersForDepartment = computed(() =>
  workCenters.value.filter((wc) => wc.departmentId === departmentId)
);

const partsForDepartment = computed(() =>
  parts.value.filter((p) => p.departmentId === departmentId)
);

const floorZonesForDepartment = computed(() =>
  floorZones.value.filter((z) => z.departmentId === departmentId)
);

function goBack() {
  router.push({ name: "departments" });
}

function goToWorkCenter(id: number) {
  router.push({ name: "work-center-detail", params: { id } });
}

function goToPart(id: number) {
  router.push({ name: "part-detail", params: { id } });
}

async function loadData() {
  loading.value = true;
  errorMessage.value = null;

  const query = `
    query DepartmentDetail($id: Int!) {
      department(id: $id) {
        id
        title
        description
      }
      workCenters {
        id
        name
        code
        departmentId
      }
      parts {
        id
        name
        departmentId
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
      department: Department;
      workCenters: WorkCenter[];
      parts: Part[];
      floorZones: FloorZone[];
    };

    const data = await fetchGraphQL<Response>(query, { id: departmentId });
    department.value = data.department ?? null;
    workCenters.value = data.workCenters ?? [];
    parts.value = data.parts ?? [];
    floorZones.value = data.floorZones ?? [];

    if (!department.value) {
      errorMessage.value = `Department ${departmentId} not found`;
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

.header-stats {
  display: flex;
  gap: 1rem;
}

.stat {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #ddd;
  background: #fafafa;
  min-width: 90px;
}

.stat-label {
  font-size: 0.75rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 600;
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

.row-clickable {
  cursor: pointer;
}

.row-clickable:hover {
  background-color: #f0f4ff;
}

.tag {
  font-size: 0.75rem;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
  border: 1px solid #ccc;
}
</style>