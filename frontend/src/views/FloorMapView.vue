<template>
  <div class="floor-map-page">
    <header class="floor-map-header">
      <div class="title-block">
        <h1>Shop Floor Layout</h1>
        <p v-if="selectedFloor">
          Viewing floor:
          <strong>{{ selectedFloor.name }}</strong>
        </p>
      </div>

      <div class="controls">
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
          v-if="zonesForFloor.length"
          class="floor-map-svg"
          viewBox="0 0 1000 600"
          preserveAspectRatio="xMidYMid meet"
        >
          <g
            v-for="zone in zonesForFloor"
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
        </svg>

        <div v-else class="no-zones">
          <p>No zones defined for this floor yet.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchGraphQL } from "@/services/graphql";

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

const route = useRoute();
const router = useRouter();

const floors = ref<Floor[]>([]);
const floorZones = ref<FloorZone[]>([]);
const selectedFloorId = ref<number | null>(null);
const highlightedWorkCenterId = ref<number | null>(null);
const loading = ref(false);
const errorMessage = ref<string | null>(null);

const selectedFloor = computed(() =>
  floors.value.find((f) => f.id === selectedFloorId.value) || null
);

const zonesForFloor = computed(() =>
  floorZones.value.filter((z) => z.floorId === selectedFloorId.value)
);



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
      }
    `;

    type Response = {
      floors: Floor[];
      floorZones: FloorZone[];
    };

    const data = await fetchGraphQL<Response>(query);
    floors.value = data.floors ?? [];
    floorZones.value = data.floorZones ?? [];

    if (!selectedFloorId.value && floors.value.length) {
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
  if (t === "work_center") return "zone-work-center";
  if (t === "department") return "zone-department";
  return "zone-other";
}

/**
 * Handle click on a zone: drill into work center or department views.
 * Adjust route names/paths to match your existing router config.
 */
function handleZoneClick(zone: FloorZone) {
  if (zone.zoneType === "work_center" && zone.workCenterId) {
    router.push({ name: "work-center-detail", params: { id: zone.workCenterId } });
    return;
  }

  if (zone.zoneType === "department" && zone.departmentId) {
    console.info("Clicked department zone", zone.departmentId);
    return;
  }

  // For zones with no binding yet, you might open a side panel or editor later
  console.info("Clicked zone", zone);
}

onMounted(() => {
  const q = route.query.workCenterId;
  if (typeof q === "string") {
    const parsed = Number(q);
    if (!Number.isNaN(parsed)) {
      highlightedWorkCenterId.value = parsed;
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
  gap: 1.5rem;
  align-items: stretch;
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

.floor-map-canvas-wrapper {
  flex: 1;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #fafafa;
  padding: 1rem;
  display: flex;
  align-items: stretch;
  justify-content: center;
}

.floor-map-svg {
  width: 100%;
  height: 100%;
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
</style>