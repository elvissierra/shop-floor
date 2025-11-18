// GraphQL service (replaces REST) — no extra deps required

const API_URL = import.meta?.env?.VITE_API_URL ?? '/graphql';

async function gql(query, variables = {}) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });
  let json;
  try {
    json = await res.json();
  } catch {
    const err = new Error(`HTTP ${res.status}`);
    err.code = 'NETWORK';
    throw err;
  }
  if (json?.errors?.length) {
    const gErr = json.errors[0] || {};
    const err = new Error(gErr.message || `HTTP ${res.status}`);
    err.code = gErr.extensions?.code || 'GRAPHQL_ERROR';
    throw err;
  }
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status}`);
    err.code = 'HTTP_ERROR';
    throw err;
  }
  return json.data;
}

// Map GraphQL part fields, tolerate camelCase or snake_case
function mapPart(gqlPart) {
  return {
    id: gqlPart.id,
    name: gqlPart.name,
    // accept either camelCase or snake_case from the API
    departmentId: gqlPart.departmentId ?? gqlPart.department_id ?? null,
  };
}

function mapWorkCenter(gqlWC) {
  return {
    id: gqlWC.id,
    name: gqlWC.name,
    code: gqlWC.code ?? null,
    // accept either camelCase or snake_case from the API
    departmentId: gqlWC.departmentId ?? gqlWC.department_id ?? null,
  };
}

export const shopFloorService = {
  // --- Departments ---
  async getDepartments({ limit = 50, offset = 0 } = {}) {
    const data = await gql(/* GraphQL */ `
      query GetDepartments($limit: Int, $offset: Int) {
        departments(limit: $limit, offset: $offset) { id title description }
      }
    `, { limit, offset });
    return data.departments;
  },

  async createDepartment(departmentData) {
    const data = await gql(/* GraphQL */ `
      mutation CreateDepartment($data: DepartmentInput!) {
        addDepartment(departmentData: $data) { id title description }
      }
    `, { data: departmentData });
    return data.addDepartment;
  },

  async updateDepartment(id, departmentData) {
    const data = await gql(/* GraphQL */ `
      mutation UpdateDepartment($id: Int!, $data: DepartmentInput!) {
        updateDepartment(id: $id, data: $data) { id title description }
      }
    `, { id, data: departmentData });
    return data.updateDepartment;
  },

  async deleteDepartment(id) {
    const data = await gql(/* GraphQL */ `
      mutation DeleteDepartment($id: Int!) {
        deleteDepartment(id: $id)
      }
    `, { id });
    return data.deleteDepartment; // boolean
  },

  // --- Work Centers ---
  async getWorkCenters({ limit = 50, offset = 0 } = {}) {
    const data = await gql(/* GraphQL */ `
      query GetWorkCenters($limit: Int, $offset: Int) {
        workCenters(limit: $limit, offset: $offset) {
          id
          name
          code
          departmentId
        }
      }
    `, { limit, offset });
    return (data.workCenters || []).map(mapWorkCenter);
  },

  async createWorkCenter(data) {
    const payload = {
      ...data,
      // normalize departmentId naming across callers
      departmentId: data.departmentId ?? data.department_id ?? null,
    };
    const result = await gql(/* GraphQL */ `
      mutation AddWorkCenter($data: WorkCenterInput!) {
        addWorkCenter(data: $data) {
          id
          name
          code
          departmentId
        }
      }
    `, { data: payload });
    return mapWorkCenter(result.addWorkCenter);
  },

  async addWorkCenter(data) {
    return this.createWorkCenter(data);
  },

  // --- Parts ---
  async getParts({ limit = 50, offset = 0 } = {}) {
    const data = await gql(/* GraphQL */ `
      query GetParts($limit: Int, $offset: Int) {
        parts(limit: $limit, offset: $offset) { id name departmentId }
      }
    `, { limit, offset });
    return data.parts.map(mapPart);
  },

  async createPart(partData) {
    // send departmentId to GraphQL API
    const payload = {
      ...partData,
      departmentId: partData.departmentId ?? partData.department_id ?? null,
    }
    const data = await gql(/* GraphQL */ `
      mutation CreatePart($data: PartInput!) {
        addPart(partData: $data) { id name departmentId }
      }
    `, { data: payload });
    return mapPart(data.addPart);
  },
  async addPart(partData) {
    return this.createPart(partData);
  },

  // --- Quality (example) ---
  async getQuality(partId) {
    const data = await gql(/* GraphQL */ `
      query GetQualitiesByPart($id: Int!) {
        part(id: $id) { id name }
        qualities { id passFail defectCount partId }
      }
    `, { id: partId });
    const qualities = (data.qualities || []).map(q => ({
      id: q.id,
      pass_fail: q.passFail ?? q.pass_fail,
      defect_count: q.defectCount ?? q.defect_count,
      part_id: q.partId ?? q.part_id,
    }));
    return qualities.filter(q => q.part_id === partId);
  },


  // --- Manufacturing methods removed (not backed by schema) ---


  // --- Dashboard rollup (used by ShopFloorView) ---
  async getShopFloorData() {
    const data = await gql(/* GraphQL */ `
      query DashboardData {
        departments { id title description }
        parts { id name departmentId }
      }
    `);
    return {
      departments: data.departments,
      parts: data.parts.map(mapPart),
    };
  },

  // --- Example update hook (stub) ---
  async updateShopFloorData(payload) {
    // Implement a real mutation when you know what aggregate you want to update
    return this.getShopFloorData();
  },
};

export default shopFloorService;