<template>
  <div class="floor-map-page">
    <header class="floor-map-header">
      <div class="title-block">
        <h1>Shop Floor Map</h1>
        <p>
          Use the map to see where departments and work centers live in your facility.
          <template v-if="selectedFloor">
            Currently viewing floor: <strong>{{ selectedFloor.name }}</strong>
          </template>
        </p>
      </div>

      <div class="controls">
        <button
          type="button"
          class="btn-secondary"
          @click="openAddFloor"
        >
          + Add floor
        </button>
        <label v-if="floors.length > 1" class="control">
          Floor
          <select v-model.number="selectedFloorId">
            <option
              v-for="floor in floors"
              :key="floor.id"
              :value="floor.id"
            >
              {{ floor.name }}
            </option>
          </select>
        </label>
      </div>
    </header>

    <section class="floor-map-body">
      <div v-if="loading" class="status">Loading floor layout…</div>
      <div v-else-if="errorMessage" class="status status-error">
        {{ errorMessage }}
      </div>
      <div
        v-else-if="selectedFloor"
        class="floor-summary"
      >
        <p class="floor-summary-text">
          {{ zoneStatsForFloor.total }} zone<span v-if="zoneStatsForFloor.total !== 1">s</span>
          on {{ selectedFloor.name }}
          <span v-if="zoneStatsForFloor.wc || zoneStatsForFloor.dept">
            • {{ zoneStatsForFloor.wc }} linked to work centers
            • {{ zoneStatsForFloor.dept }} linked to departments
          </span>
        </p>
      </div>
      <div class="floor-map-layout">
        <div class="floor-map-legend">
          <h2>Legend</h2>
          <ul>
            <li><span class="legend-swatch legend-work-center"></span> Work Center</li>
            <li><span class="legend-swatch legend-department"></span> Department</li>
            <li><span class="legend-swatch legend-other"></span> Other</li>
          </ul>
        </div>

        <div class="floor-map-canvas-wrapper">
          <svg
            class="floor-map-svg"
            viewBox="0 0 1000 600"
            preserveAspectRatio="xMidYMid meet"
            @click="handleCanvasClick"
          >
            <g
              v-for="zone in sortedZonesForFloor"
              :key="zone.id"
              class="floor-zone-group"
              @click="handleZoneClick(zone)"
            >
              <polygon
                class="floor-zone"
                :class="zoneCssClass(zone)"
                :points="zonePolygonPoints(zone)"
              />
              <text
                class="floor-zone-label"
                :x="zoneLabelPosition(zone).x"
                :y="zoneLabelPosition(zone).y"
              >
                {{ zone.name }}
              </text>
            </g>

            <!-- Draft polygon preview while drawing a new zone -->
            <polyline
              v-if="drawingMode && draftPoints.length"
              class="floor-zone draft-zone"
              :points="draftPolygonPoints"
            />
            <g v-if="drawingMode">
              <circle
                v-for="(pt, idx) in draftPoints"
                :key="idx"
                class="draft-point"
                :cx="pt.x"
                :cy="pt.y"
                r="6"
              />
            </g>
          </svg>

          <div
            v-if="!zonesForFloor.length && !draftPoints.length"
            class="no-zones"
          >
            <p>No zones defined for this floor yet.</p>
          </div>
        </div>
      </div>
    </section>
    <section class="floor-map-zones">
      <div v-if="selectedZone" class="zone-inspector">
        <h3>Selected zone</h3>
        <p class="zone-name">{{ selectedZone.name }}</p>
        <p>
          Floor: {{ floorLabel(selectedZone.floorId) }}
          <span v-if="selectedZone.zoneType">
            •
            {{
              selectedZone.zoneType === 'work_center'
                ? 'Work Center'
                : selectedZone.zoneType === 'department'
                ? 'Department'
                : selectedZone.zoneType
            }}
          </span>
        </p>
        <p v-if="selectedZone.workCenterId">
          Work Center:
          <button type="button" @click="openWorkCenter(selectedZone.workCenterId!)">
            Open work center
          </button>
        </p>
        <p v-if="selectedZone.departmentId">
          Department:
          <button type="button" @click="openDepartment(selectedZone.departmentId!)">
            Open department
          </button>
        </p>
        <p
          v-if="!selectedZone.workCenterId && !selectedZone.departmentId"
          class="zone-inspector-muted"
        >
          This zone is not linked to a department or work center yet.
        </p>
      </div>

      <div class="zone-list-header">
        <h3>Zones on this floor</h3>
        <button type="button" class="btn-secondary" @click="openAddZone">
          + Add zone
        </button>
      </div>
      <div v-if="drawingMode" class="drawing-hint">
        <p>
          Click on the map to add corners for the new zone.
        </p>
        <div class="drawing-actions">
          <button type="button" class="btn-secondary" @click="finishDrawing">
            Finish polygon
          </button>
          <button type="button" class="btn-secondary" @click="cancelDrawing">
            Cancel
          </button>
        </div>
      </div>
      <ul v-if="zonesForFloor.length" class="zone-list">
        <li
          v-for="zone in zonesForFloor"
          :key="zone.id"
          :class="[
            'zone-list-item',
            { active: selectedZone && selectedZone.id === zone.id }
          ]"
          @click="handleZoneClick(zone)"
        >
          <div class="zone-list-name">{{ zone.name }}</div>
          <div class="zone-list-meta">
            Floor: {{ floorLabel(zone.floorId) }}
            <span v-if="zone.zoneType">
              •
              {{
                zone.zoneType === 'work_center'
                  ? 'Work Center'
                  : zone.zoneType === 'department'
                  ? 'Department'
                  : zone.zoneType
              }}
            </span>
          </div>
        </li>
      </ul>
      <p v-else class="zone-list-empty">
        No zones defined for this floor yet.
      </p>
    </section>
        <Modal v-if="showZoneModal" @cancel="closeZoneModal">
      <template #title>New zone</template>
      <form class="form" @submit.prevent="saveZone">
        <div class="field">
          <label for="zone-name">Name <span class="req">*</span></label>
          <input
            id="zone-name"
            v-model.trim="zoneForm.name"
            type="text"
            required
            :disabled="zoneSubmitting"
            autocomplete="off"
          />
        </div>

        <div class="field">
          <label for="zone-floor">Floor</label>
          <select
            id="zone-floor"
            v-model.number="zoneForm.floorId"
            :disabled="zoneSubmitting"
          >
            <option
              v-for="floor in floors"
              :key="floor.id"
              :value="floor.id"
            >
              {{ floor.name }}
            </option>
          </select>
        </div>

        <div class="field">
          <label for="zone-type">Zone type</label>
          <select
            id="zone-type"
            v-model="zoneForm.zoneType"
            :disabled="zoneSubmitting"
          >
            <option disabled value="">
              Select zone type
            </option>
            <option value="work_center">Work center</option>
            <option value="department">Department</option>
            <option value="other">Other (not tied to a specific object)</option>
          </select>
        </div>

        <div class="field">
          <label for="zone-work-center">Work center</label>
          <select
            id="zone-work-center"
            v-model.number="zoneForm.workCenterId"
            :disabled="zoneSubmitting"
          >
            <option :value="null">Unassigned</option>
            <option
              v-for="wc in workCenters"
              :key="wc.id"
              :value="wc.id"
            >
              #{{ wc.id }} — {{ wc.name }}
            </option>
          </select>
        </div>

        <div class="field">
          <label for="zone-department">Department</label>
          <select
            id="zone-department"
            v-model.number="zoneForm.departmentId"
            :disabled="zoneSubmitting"
          >
            <option :value="null">Unassigned</option>
            <option
              v-for="d in departments"
              :key="d.id"
              :value="d.id"
            >
              {{ d.title }}
            </option>
          </select>
        </div>

        <div class="field">
          <label for="zone-polygon">Polygon</label>
          <textarea
            id="zone-polygon"
            v-model.trim="zoneForm.polygon"
            rows="3"
            :disabled="zoneSubmitting"
            placeholder="Normally filled by drawing on the map. Advanced users can edit coordinates here."
          ></textarea>
          <small class="help-text">
            Coordinates are stored in the format "x1,y1 x2,y2 …" within the 0–1000 × 0–600 canvas.
          </small>
        </div>

        <div class="actions">
          <button
            type="button"
            class="btn"
            @click="closeZoneModal"
            :disabled="zoneSubmitting"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn primary"
            :disabled="zoneSubmitting"
          >
            <span v-if="zoneSubmitting">Saving…</span>
            <span v-else>Save</span>
          </button>
        </div>
      </form>
    </Modal>
    <Modal v-if="showFloorModal" @cancel="closeFloorModal">
      <template #title>New floor</template>
      <form class="form" @submit.prevent="saveFloor">
        <div class="field">
          <label for="floor-name">Name <span class="req">*</span></label>
          <input
            id="floor-name"
            v-model.trim="floorForm.name"
            type="text"
            required
            :disabled="floorSubmitting"
            autocomplete="off"
          />
        </div>
        <div class="field">
          <label for="floor-description">Description</label>
          <textarea
            id="floor-description"
            v-model.trim="floorForm.description"
            rows="3"
            :disabled="floorSubmitting"
          ></textarea>
        </div>
        <div class="actions">
          <button
            type="button"
            class="btn"
            @click="closeFloorModal"
            :disabled="floorSubmitting"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn primary"
            :disabled="floorSubmitting || !floorForm.name"
          >
            <span v-if="floorSubmitting">Saving…</span>
            <span v-else>Save</span>
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchGraphQL } from "@/services/graphql";
import Modal from "@/components/Modal.vue";
import { useToast } from "../composables/useToast";

const CANVAS_WIDTH = 1000;
const CANVAS_HEIGHT = 600;
const GRID_STEP_X = 25;
const GRID_STEP_Y = 25;

type Floor = {
  id: number;
  name: string;
  description?: string | null;
};

type FloorZone = {
  id: number;
  floorId: number;
  name: string;
  zoneType?: string | null;
  departmentId?: number | null;
  workCenterId?: number | null;
  polygon: string; // "x1,y1 x2,y2 ..."
};

type Department = {
  id: number;
  title: string;
};

type WorkCenter = {
  id: number;
  name: string;
  code: string | null;
  departmentId: number | null;
};

type FloorZoneForm = {
  floorId: number | null;
  name: string;
  zoneType: string;
  departmentId: number | null;
  workCenterId: number | null;
  polygon: string;
};

type FloorForm = {
  name: string;
  description: string;
};
const route = useRoute();
const router = useRouter();

const floors = ref<Floor[]>([]);
const floorZones = ref<FloorZone[]>([]);

const floorNameLookup = computed(() => {
  const map = new Map<number, string>();
  for (const f of floors.value) {
    map.set(f.id, f.name);
  }
  return map;
});

function floorLabel(floorId: number | null): string {
  if (floorId == null) return "—";
  return floorNameLookup.value.get(floorId) ?? `Floor ${floorId}`;
}
const selectedFloorId = ref<number | null>(null);
const highlightedWorkCenterId = ref<number | null>(null);
const highlightedDepartmentId = ref<number | null>(null);
const loading = ref(false);
const errorMessage = ref<string | null>(null);
const selectedZone = ref<FloorZone | null>(null);

const departments = ref<Department[]>([]);
const workCenters = ref<WorkCenter[]>([]);
const drawingMode = ref(false);
const draftPoints = ref<{ x: number; y: number }[]>([]);

const showZoneModal = ref(false);
const zoneSubmitting = ref(false);
const zoneForm = ref<FloorZoneForm>({
  floorId: null,
  name: "",
  zoneType: "",
  departmentId: null,
  workCenterId: null,
  polygon: "",
});

const showFloorModal = ref(false);
const floorSubmitting = ref(false);
const floorForm = ref<FloorForm>({
  name: "",
  description: "",
});

const { push: toast } = useToast();

const selectedFloor = computed(() =>
  floors.value.find((f) => f.id === selectedFloorId.value) || null
);

const zonesForFloor = computed(() =>
  floorZones.value.filter((z) => z.floorId === selectedFloorId.value)
);

const sortedZonesForFloor = computed(() => {
  const zones = zonesForFloor.value.slice();
  zones.sort((a, b) => zoneDrawOrder(a) - zoneDrawOrder(b));
  return zones;
});

const zoneStatsForFloor = computed(() => {
  const zones = zonesForFloor.value;
  const total = zones.length;
  let wc = 0;
  let dept = 0;

  for (const z of zones) {
    if (z.workCenterId != null) wc += 1;
    if (z.departmentId != null) dept += 1;
  }

  return { total, wc, dept };
});

const draftPolygonPoints = computed(() =>
  draftPoints.value
    .map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`)
    .join(" ")
);

function openAddFloor() {
  floorForm.value = {
    name: "",
    description: "",
  };
  showFloorModal.value = true;
}

function closeFloorModal() {
  showFloorModal.value = false;
}

async function saveFloor() {
  if (!floorForm.value.name.trim()) {
    toast({
      type: "error",
      title: "Missing name",
      message: "Give the floor a name.",
    });
    return;
  }

  try {
    floorSubmitting.value = true;

    const mutation = `
      mutation AddFloor($data: FloorInput!) {
        addFloor(data: $data) {
          id
          name
          description
        }
      }
    `;

    const payload = {
      name: floorForm.value.name.trim(),
      description: floorForm.value.description.trim() || null,
    };

    type FloorMutationResponse = { addFloor: Floor };
    const data = await fetchGraphQL<FloorMutationResponse>(mutation, {
      data: payload,
    });

    floors.value.push(data.addFloor);
    selectedFloorId.value = data.addFloor.id;

    toast({
      type: "success",
      title: "Floor created",
      message: data.addFloor.name,
    });
    showFloorModal.value = false;
  } catch (err: any) {
    console.error(err);
    const message = err?.message ?? String(err);
    errorMessage.value = message;
    const code = (err as any)?.code;
    toast({
      type: "error",
      title: "Save failed",
      message: code ? `${code}: ${message}` : message,
    });
  } finally {
    floorSubmitting.value = false;
  }
}

async function loadFloorsAndZones() {
  loading.value = true;
  errorMessage.value = null;
  try {
    const query = `
      query FloorMapData {
        floors {
          id
          name
          description
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
        departments {
          id
          title
        }
        workCenters {
          id
          name
          code
          departmentId
        }
      }
    `;

    type Response = {
      floors: Floor[];
      floorZones: FloorZone[];
      departments: Department[];
      workCenters: WorkCenter[];
    };

    const data = await fetchGraphQL<Response>(query);
    floors.value = data.floors ?? [];
    floorZones.value = data.floorZones ?? [];
    departments.value = data.departments ?? [];
    workCenters.value = data.workCenters ?? [];

    // If a specific work center or department is highlighted, try to select
    // the floor that contains its zone; otherwise fall back to the first floor.
    if (highlightedWorkCenterId.value || highlightedDepartmentId.value) {
      const targetZone = floorZones.value.find((z) => {
        if (
          highlightedWorkCenterId.value &&
          z.workCenterId === highlightedWorkCenterId.value
        ) {
          return true;
        }
        if (
          highlightedDepartmentId.value &&
          z.departmentId === highlightedDepartmentId.value
        ) {
          return true;
        }
        return false;
      });
      if (targetZone) {
        selectedFloorId.value = targetZone.floorId;
      } else if (!selectedFloorId.value && floors.value.length) {
        selectedFloorId.value = floors.value[0].id;
      }
    } else if (!selectedFloorId.value && floors.value.length) {
      selectedFloorId.value = floors.value[0].id;
    }
  } catch (err: any) {
    errorMessage.value = err?.message ?? String(err);
    console.error("Failed to load floor map data", err);
  } finally {
    loading.value = false;
  }
}

/**
 * Convert polygon string ("x1,y1 x2,y2 ...") to SVG points attribute.
 */
function zonePolygonPoints(zone: FloorZone): string {
  return zone.polygon;
}


/**
 * Very simple heuristic: take the average of the polygon points as label center.
 */
function zoneLabelPosition(zone: FloorZone): { x: number; y: number } {
  const raw = zone.polygon.trim();
  const parts = raw.split(/\s+/);
  let sumX = 0;
  let sumY = 0;
  let count = 0;

  for (const p of parts) {
    const [xs, ys] = p.split(",");
    const x = Number(xs);
    const y = Number(ys);
    if (!Number.isNaN(x) && !Number.isNaN(y)) {
      sumX += x;
      sumY += y;
      count += 1;
    }
  }

  if (!count) return { x: 0, y: 0 };
  return { x: sumX / count, y: sumY / count };
}

function zoneCssClass(zone: FloorZone): string {
  const t = zone.zoneType || "";
  if (highlightedWorkCenterId.value && zone.workCenterId === highlightedWorkCenterId.value) {
    return "zone-highlight";
  }
  if (highlightedDepartmentId.value && zone.departmentId === highlightedDepartmentId.value) {
    return "zone-highlight";
  }
  if (t === "work_center") return "zone-work-center";
  if (t === "department") return "zone-department";
  return "zone-other";
}

function zoneDrawOrder(zone: FloorZone): number {
  const t = zone.zoneType || "";
  if (t === "department") return 0; // draw first, behind others
  if (t === "other") return 1;
  if (t === "work_center") return 2;
  return 1;
}

function handleZoneClick(zone: FloorZone) {
  if (drawingMode.value) return;
  selectedZone.value = zone;
}

function openWorkCenter(id: number) {
  router.push({ name: "work-center-detail", params: { id } });
}

function openDepartment(id: number) {
  router.push({ name: "department-detail", params: { id } });
}

function openAddZone() {
  if (!floors.value.length) {
    toast({
      type: "error",
      title: "No floors available",
      message: "Create a floor before adding zones.",
    });
    return;
  }

  const floorId = selectedFloorId.value ?? floors.value[0].id;
  const inferredType =
    highlightedWorkCenterId.value != null
      ? "work_center"
      : highlightedDepartmentId.value != null
      ? "department"
      : "";

  zoneForm.value = {
    floorId,
    name: "",
    zoneType: inferredType,
    departmentId: highlightedDepartmentId.value ?? null,
    workCenterId: highlightedWorkCenterId.value ?? null,
    polygon: "",
  };

  selectedFloorId.value = floorId;
  draftPoints.value = [];
  drawingMode.value = true;

  toast({
    type: "info",
    title: "Drawing zone",
    message: "Click on the map to add corners. When finished, use 'Finish polygon'.",
  });
}

function closeZoneModal() {
  showZoneModal.value = false;
}

function handleCanvasClick(event: MouseEvent) {
  if (!drawingMode.value) return;

  const svg = event.currentTarget as SVGSVGElement | null;
  if (!svg) return;

    const rect = svg.getBoundingClientRect();
  const xNorm = (event.clientX - rect.left) / rect.width;
  const yNorm = (event.clientY - rect.top) / rect.height;

  const rawX = xNorm * CANVAS_WIDTH;
  const rawY = yNorm * CANVAS_HEIGHT;

  // Snap to a simple grid so shapes stay tidy and aligned
  const snappedX = Math.round(rawX / GRID_STEP_X) * GRID_STEP_X;
  const snappedY = Math.round(rawY / GRID_STEP_Y) * GRID_STEP_Y;

  // Clamp in case rounding pushes us out of bounds
  const x = Math.min(Math.max(snappedX, 0), CANVAS_WIDTH);
  const y = Math.min(Math.max(snappedY, 0), CANVAS_HEIGHT);

  draftPoints.value.push({ x, y });
}

function cancelDrawing() {
  drawingMode.value = false;
  draftPoints.value = [];
}

function finishDrawing() {
  if (draftPoints.value.length < 3) {
    toast({
      type: "error",
      title: "Polygon too small",
      message: "Add at least three corners to define a zone.",
    });
    return;
  }

  // Convert draft points to the persisted polygon string
  zoneForm.value.polygon = draftPolygonPoints.value;
  drawingMode.value = false;

  toast({
    type: "success",
    title: "Shape captured",
    message: "Now name the zone and link it to a department or work center.",
  });

  showZoneModal.value = true;
}

async function saveZone() {
  if (!zoneForm.value.floorId) {
    toast({
      type: "error",
      title: "Missing floor",
      message: "Select a floor for this zone.",
    });
    return;
  }

  if (!zoneForm.value.name.trim()) {
    toast({
      type: "error",
      title: "Missing name",
      message: "Give the zone a name.",
    });
    return;
  }

  if (!zoneForm.value.polygon.trim()) {
    toast({
      type: "error",
      title: "Missing shape",
      message: "Draw the zone on the map or enter coordinates.",
    });
    return;
  }

  const zoneType = zoneForm.value.zoneType;
  const hasWorkCenter = zoneForm.value.workCenterId != null;
  const hasDepartment = zoneForm.value.departmentId != null;

  // Enforce correlation between zone type and linked model
  if (zoneType === "work_center" && !hasWorkCenter) {
    toast({
      type: "error",
      title: "Work center required",
      message:
        "Choose a work center for this zone or change the type to Other.",
    });
    return;
  }

  if (zoneType === "department" && !hasDepartment) {
    toast({
      type: "error",
      title: "Department required",
      message:
        "Choose a department for this zone or change the type to Other.",
    });
    return;
  }

  if (!zoneType && (hasWorkCenter || hasDepartment)) {
    toast({
      type: "error",
      title: "Zone type required",
      message:
        "Select whether this zone represents a work center or department, or set the type to Other.",
    });
    return;
  }

  try {
    zoneSubmitting.value = true;

    const mutation = `
      mutation AddFloorZone($data: FloorZoneInput!) {
        addFloorZone(data: $data) {
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

    const normalizedZoneType = zoneForm.value.zoneType || null;
    let departmentId = zoneForm.value.departmentId ?? null;
    let workCenterId = zoneForm.value.workCenterId ?? null;

    // Enforce that each zone type links appropriately:
    // - work_center: only workCenterId
    // - department: only departmentId
    // - other: no links
    if (normalizedZoneType === "work_center") {
      departmentId = null;
    } else if (normalizedZoneType === "department") {
      workCenterId = null;
    } else if (normalizedZoneType === "other") {
      departmentId = null;
      workCenterId = null;
    }

    const payload = {
      floorId: zoneForm.value.floorId,
      name: zoneForm.value.name.trim(),
      zoneType: normalizedZoneType,
      departmentId,
      workCenterId,
      polygon: zoneForm.value.polygon.trim(),
    };

    type MutationResponse = { addFloorZone: FloorZone };
    const data = await fetchGraphQL<MutationResponse>(mutation, { data: payload });

    // Update local state so SVG and list reflect the new zone immediately
    floorZones.value.push(data.addFloorZone);
    selectedZone.value = data.addFloorZone;
    if (!selectedFloorId.value) {
      selectedFloorId.value = data.addFloorZone.floorId;
    }

    toast({
      type: "success",
      title: "Zone added",
      message: data.addFloorZone.name,
    });
    showZoneModal.value = false;
  } catch (err: any) {
    console.error(err);
    const message = err?.message ?? String(err);
    errorMessage.value = message;
    const code = (err as any)?.code;
    toast({
      type: "error",
      title: "Save failed",
      message: code ? `${code}: ${message}` : message,
    });
  } finally {
    zoneSubmitting.value = false;
  }
}

onMounted(() => {
  const wc = route.query.workCenterId;
  if (typeof wc === "string") {
    const parsed = Number(wc);
    if (!Number.isNaN(parsed)) {
      highlightedWorkCenterId.value = parsed;
    }
  }

  const dept = route.query.departmentId;
  if (typeof dept === "string") {
    const parsed = Number(dept);
    if (!Number.isNaN(parsed)) {
      highlightedDepartmentId.value = parsed;
    }
  }

  loadFloorsAndZones();
});
</script>

<style scoped>
.floor-map-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem 2rem;
}

.floor-map-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem;
}

.title-block h1 {
  margin: 0;
  font-size: 1.6rem;
}

.title-block p {
  margin: 0.25rem 0 0;
  color: #666;
}

.controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.control label {
  font-size: 0.9rem;
}

.control {
  font-size: 0.9rem;
}


.floor-map-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: stretch;
}

.floor-map-layout {
  display: flex;
  gap: 1.5rem;
  align-items: stretch;
}

.floor-summary {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #374151;
}

.floor-summary-text {
  margin: 0;
}

.floor-map-legend {
  min-width: 200px;
}

.floor-map-legend h2 {
  margin-top: 0;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.floor-map-legend ul {
  list-style: none;
  padding: 0;
  margin: 0.75rem 0 0;
}

.floor-map-legend li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.35rem;
}

.legend-swatch {
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 2px;
  border: 1px solid rgba(0, 0, 0, 0.2);
}

.legend-work-center {
  background-color: rgba(0, 150, 255, 0.25);
}

.legend-department {
  background-color: rgba(0, 200, 120, 0.25);
}

.legend-other {
  background-color: rgba(180, 180, 180, 0.25);
}

.zone-inspector {
  margin-top: 1.25rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
  font-size: 0.9rem;
}

.zone-inspector h3 {
  margin: 0 0 0.25rem;
  font-size: 0.95rem;
}

.zone-name {
  margin: 0.1rem 0;
  font-weight: 600;
}

.zone-inspector p {
  margin: 0.15rem 0;
}

.zone-inspector-muted {
  color: #6b7280;
  font-size: 0.85rem;
}

.zone-inspector button {
  border: none;
  border-radius: 999px;
  padding: 0.25rem 0.7rem;
  font-size: 0.85rem;
  cursor: pointer;
  background: #e5e7eb;
}

.zone-inspector button:hover {
  background: #d4d4d8;
}

.zone-list-header {
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.zone-list-header h3 {
  margin: 0;
  font-size: 0.95rem;
}

.zone-list {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0;
  max-height: 260px;
  overflow-y: auto;
}

.zone-list-item {
  padding: 0.35rem 0;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
}

.zone-list-item:last-child {
  border-bottom: none;
}

.zone-list-item.active {
  background: #eef2ff;
}

.zone-list-name {
  font-size: 0.9rem;
  font-weight: 500;
}

.zone-list-meta {
  font-size: 0.8rem;
  color: #6b7280;
}

.zone-list-empty {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #6b7280;
}

.drawing-hint {
  margin-top: 0.75rem;
  padding: 0.5rem 0.6rem;
  border-radius: 6px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  font-size: 0.85rem;
  color: #1e3a8a;
}

.drawing-hint p {
  margin: 0 0 0.35rem;
}

.drawing-actions {
  display: flex;
  gap: 0.5rem;
}

.draft-zone {
  fill: none;
  stroke: #6366f1;
  stroke-width: 2;
  stroke-dasharray: 4 2;
}

.draft-point {
  fill: #ffffff;
  stroke: #6366f1;
  stroke-width: 2;
}

.btn-secondary {
  border: none;
  border-radius: 999px;
  padding: 0.25rem 0.8rem;
  cursor: pointer;
  background: #e5e7eb;
  font-size: 0.8rem;
  white-space: nowrap;
}

.btn-secondary:hover {
  background: #d4d4d8;
}

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
.form select,
.form textarea {
  border: 1px solid var(--c-border);
  border-radius: 8px;
  padding: 0.5rem 0.6rem;
  background: #fff;
  font: inherit;
}

.help-text {
  font-size: 0.8rem;
  color: #6b7280;
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
  font-size: 0.9rem;
}

.btn.primary {
  background: var(--c-primary);
  color: #fff;
}

.floor-map-canvas-wrapper {
  flex: 1;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #f9fafb;
  padding: 1rem;
  display: flex;
  align-items: stretch;
  justify-content: center;
}

.floor-map-svg {
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(to right, #e5e7eb 1px, transparent 1px),
    linear-gradient(to bottom, #e5e7eb 1px, transparent 1px);
  background-size:25px 25px;
}

.floor-zone-group {
  cursor: pointer;
}

.floor-zone {
  stroke: #555;
  stroke-width: 1;
  fill-opacity: 0.4;
  transition: transform 0.1s ease, fill-opacity 0.1s ease, stroke-width 0.1s ease;
}

.floor-zone-group:hover .floor-zone {
  fill-opacity: 0.7;
  stroke-width: 2;
}

.zone-work-center {
  fill: rgba(0, 150, 255, 0.4);
}

.zone-department {
  fill: rgba(0, 200, 120, 0.4);
}

.zone-other {
  fill: rgba(180, 180, 180, 0.4);
}

.floor-zone-label {
  font-size: 12px;
  text-anchor: middle;
  dominant-baseline: middle;
  fill: #222;
  pointer-events: none;
}

.no-zones {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: #777;
}

.status {
  margin-bottom: 0.75rem;
  color: #555;
}

.status-error {
  color: #b00020;
}

.zone-highlight {
  stroke-width: 3;
  fill-opacity: 0.75;
}

.floor-map-zones {
  margin-top: 0.75rem;
}
</style>