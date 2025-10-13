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

// Map GraphQL snake_case fields directly
function mapPart(gqlPart) {
  return { id: gqlPart.id, name: gqlPart.name, department_id: gqlPart.department_id };
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

  // --- Parts ---
  async getParts({ limit = 50, offset = 0 } = {}) {
    const data = await gql(/* GraphQL */ `
      query GetParts($limit: Int, $offset: Int) {
        parts(limit: $limit, offset: $offset) { id name department_id }
      }
    `, { limit, offset });
    return data.parts.map(mapPart);
  },

  async createPart(partData) {
    const data = await gql(/* GraphQL */ `
      mutation CreatePart($data: PartInput!) {
        addPart(partData: $data) { id name department_id }
      }
    `, { data: partData });
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
        qualities { id pass_fail defect_count part_id }
      }
    `, { id: partId });
    // Placeholder; tailor to your needs
    return data.qualities.filter(q => q.part_id === partId);
  },

  // --- Dashboard rollup (used by ShopFloorView) ---
  async getShopFloorData() {
    const data = await gql(/* GraphQL */ `
      query DashboardData {
        departments { id title description }
        parts { id name department_id }
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