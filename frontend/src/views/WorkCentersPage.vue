<template>
  <div class="page">
    <header class="page-header">
      <div>
        <h1>Work Centers</h1>
        <p class="subtitle">
          {{ centers.length }} total
        </p>
      </div>
    </header>

    <section class="content">
      <div v-if="loading" class="status">Loading work centers…</div>
      <div v-else-if="errorMessage" class="status status-error">
        {{ errorMessage }}
      </div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Code</th>
            <th>Department</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="wc in centers"
            :key="wc.id"
            @click="goToDetail(wc.id)"
            class="row-clickable"
          >
            <td>{{ wc.id }}</td>
            <td>{{ wc.name }}</td>
            <td>{{ wc.code || "—" }}</td>
            <td>{{ wc.departmentId ?? "—" }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { fetchGraphQL } from "@/services/graphql";

type WorkCenter = {
  id: number;
  name: string;
  code: string | null;
  departmentId: number | null;
};

const router = useRouter();
const centers = ref<WorkCenter[]>([]);
const loading = ref(false);
const errorMessage = ref<string | null>(null);

async function loadWorkCenters() {
  loading.value = true;
  errorMessage.value = null;

  const query = `
    query WorkCenters {
      workCenters {
        id
        name
        code
        departmentId
      }
    }
  `;

  try {
    type Response = { workCenters: WorkCenter[] };
    const data = await fetchGraphQL<Response>(query);
    centers.value = data.workCenters ?? [];
  } catch (err: any) {
    console.error(err);
    errorMessage.value = err?.message ?? String(err);
  } finally {
    loading.value = false;
  }
}

function goToDetail(id: number) {
  router.push({ name: "work-center-detail", params: { id } });
}

onMounted(loadWorkCenters);
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
  justify-content: space-between;
  align-items: flex-end;
}

.subtitle {
  margin-top: 0.25rem;
  color: #666;
  font-size: 0.9rem;
}

.content {
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #fafafa;
  padding: 1rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.table th,
.table td {
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e1e1e1;
  text-align: left;
}

.table th {
  font-weight: 600;
  color: #444;
}

.row-clickable {
  cursor: pointer;
}

.row-clickable:hover {
  background-color: #f0f4ff;
}

.status {
  padding: 0.5rem;
  color: #555;
}

.status-error {
  color: #b00020;
}
</style>