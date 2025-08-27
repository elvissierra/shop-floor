// GraphQL service (replaces REST) — no extra deps required

const API_URL = import.meta?.env?.VITE_API_URL ?? 'http://localhost:8000/graphql';

async function gql(query, variables = {}) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json?.errors?.[0]?.message || `HTTP ${res.status}`);
  if (json.errors && json.errors.length) throw new Error(json.errors[0].message);
  return json.data;
}

// Map GraphQL camelCase → current UI snake_case where needed
function mapPart(gqlPart) {
  return {
    id: gqlPart.id,
    name: gqlPart.name,
    department_id: gqlPart.departmentId, // map for current components
  };
}

export const shopFloorService = {
  // --- Departments ---
  async getDepartments() {
    const data = await gql(/* GraphQL */ `
      query GetDepartments {
        departments { id title description }
      }
    `);
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

  async deleteDepartment(id) {
    const data = await gql(/* GraphQL */ `
      mutation DeleteDepartment($id: Int!) {
        deleteDepartment(id: $id)
      }
    `, { id });
    return data.deleteDepartment; // boolean
  },

  // --- Parts ---
  async getParts() {
    const data = await gql(/* GraphQL */ `
      query GetParts {
        parts { id name departmentId }
      }
    `);
    return data.parts.map(mapPart);
  },

  async createPart(partData) {
    const data = await gql(/* GraphQL */ `
      mutation CreatePart($data: PartInput!) {
        addPart(partData: $data) { id name departmentId }
      }
    `, { data: partData });
    return mapPart(data.addPart);
  },

  // --- Quality (example) ---
  async getQuality(partId) {
    const data = await gql(/* GraphQL */ `
      query GetQualitiesByPart($id: Int!) {
        part(id: $id) { id name }
        qualities { id passFail defectCount partId }
      }
    `, { id: partId });
    // Placeholder; tailor to your needs
    return data.qualities.filter(q => q.partId === partId);
  },

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