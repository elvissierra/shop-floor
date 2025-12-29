<template>
  <div class="page">
    <header class="page-header">
      <div>
        <h1>Work Centers</h1>
        <p class="subtitle">
          {{ centers.length }} total
        </p>
      </div>
      <button class="btn-primary" @click="openCreate">+ Add Work Center</button>
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
            <td>
              <span v-if="wc.departmentId">
                {{ departmentName(wc.departmentId) || `#${wc.departmentId}` }}
              </span>
              <span v-else>—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
    <section class="map-cta" aria-label="Shop floor overview">
      <h2 class="map-cta-title">Shop floor overview</h2>
      <p class="map-cta-text">
        Open the shop floor map to see where work centers live in the plant and jump into their details.
      </p>
      <router-link class="btn-map" to="/floor-map">Open floor map</router-link>
    </section>
    <Modal v-if="showModal" @cancel="closeModal">
      <template #title>New Work Center</template>
      <form class="form" @submit.prevent="saveWorkCenter">
        <div class="field">
          <label for="wc-name">Name <span class="req">*</span></label>
          <input
            id="wc-name"
            v-model.trim="form.name"
            type="text"
            required
            :disabled="submitting"
            autocomplete="off"
          />
        </div>
        <div class="field">
          <label for="wc-code">Code</label>
          <input
            id="wc-code"
            v-model.trim="form.code"
            type="text"
            :disabled="submitting"
            autocomplete="off"
          />
        </div>
        <div class="field">
          <label for="wc-dept">Department</label>
          <select
            id="wc-dept"
            v-model.number="form.departmentId"
            :disabled="submitting"
          >
            <option :value="null">Unassigned</option>
            <option v-for="d in departmentOptions" :key="d.id" :value="d.id">
              {{ d.title }}
            </option>
          </select>
        </div>
        <div class="actions">
          <button
            type="button"
            class="btn"
            @click="closeModal"
            :disabled="submitting"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn primary"
            :disabled="submitting || !form.name"
          >
            <span v-if="submitting">Saving…</span>
            <span v-else>Save</span>
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { fetchGraphQL } from "@/services/graphql";
import Modal from "@/components/Modal.vue";
import { useToast } from "../composables/useToast";

type WorkCenter = {
  id: number;
  name: string;
  code: string | null;
  departmentId: number | null;
};

type Department = {
  id: number;
  title: string;
};

const router = useRouter();
const centers = ref<WorkCenter[]>([]);
const loading = ref(false);
const errorMessage = ref<string | null>(null);

const { push: toast } = useToast();

const showModal = ref(false);
const submitting = ref(false);

type WorkCenterForm = {
  name: string;
  code: string;
  departmentId: number | null;
};

const form = ref<WorkCenterForm>({
  name: "",
  code: "",
  departmentId: null,
});

const departmentOptions = ref<Department[]>([]);

const departmentName = (id: number | null): string | null => {
  if (id == null) return null;
  const dept = departmentOptions.value.find((d) => d.id === id);
  return dept ? dept.title : null;
};

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

async function loadDepartments() {
  const query = `
    query DepartmentsForWorkCenters {
      departments {
        id
        title
      }
    }
  `;

  try {
    type Response = { departments: Department[] };
    const data = await fetchGraphQL<Response>(query);
    departmentOptions.value = data.departments ?? [];
  } catch (err: any) {
    // Work centers list still functions without department options for the modal
    console.error(err);
  }
}

function openCreate() {
  form.value = {
    name: "",
    code: "",
    departmentId: departmentOptions.value[0]?.id ?? null,
  };
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

async function saveWorkCenter() {
  try {
    submitting.value = true;
    const mutation = `
      mutation AddWorkCenter($data: WorkCenterInput!) {
        addWorkCenter(data: $data) {
          id
          name
          code
          departmentId
        }
      }
    `;

    const payload = {
      name: form.value.name,
      code: form.value.code || null,
      departmentId: form.value.departmentId ?? null,
    };

    type Response = { addWorkCenter: WorkCenter };
    const data = await fetchGraphQL<Response>(mutation, { data: payload });

    centers.value.unshift(data.addWorkCenter);
    toast({
      type: "success",
      title: "Work center created",
      message: data.addWorkCenter.name,
    });
    closeModal();
  } catch (err: any) {
    console.error(err);
    const message = err?.message ?? String(err);
    errorMessage.value = message;
    toast({
      type: "error",
      title: "Save failed",
      message: err?.code ? `${err.code}: ${message}` : message,
    });
  } finally {
    submitting.value = false;
  }
}

function goToDetail(id: number) {
  router.push({ name: "work-center-detail", params: { id } });
}

onMounted(async () => {
  await Promise.all([loadWorkCenters(), loadDepartments()]);
});
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

.btn-primary {
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.45rem 0.9rem;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-primary:hover {
  opacity: 0.95;
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

<style scoped>
.map-cta {
  margin-top: 1.5rem;
  padding: 1.25rem 1rem;
  border-radius: 8px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem 1rem;
  justify-content: space-between;
}

.map-cta-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
}

.map-cta-text {
  margin: 0;
  flex: 1 1 260px;
  font-size: 0.95rem;
  color: #4b5563;
}

.btn-map {
  text-decoration: none;
  border: none;
  border-radius: 999px;
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  background: var(--c-primary);
  color: #fff;
  white-space: nowrap;
}

.btn-map:hover {
  opacity: 0.95;
}

@media (max-width: 640px) {
  .map-cta {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>