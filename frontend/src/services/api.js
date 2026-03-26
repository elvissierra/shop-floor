// GraphQL service — no extra deps required

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

export const shopFloorService = {
  // --- Departments ---
  async getDepartments({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetDepartments($limit: Int, $offset: Int) {
        departments(limit: $limit, offset: $offset) { id title description }
      }
    `, { limit, offset });
    return data.departments;
  },

  async createDepartment(departmentData) {
    const data = await gql(`
      mutation CreateDepartment($data: DepartmentInput!) {
        addDepartment(departmentData: $data) { id title description }
      }
    `, { data: departmentData });
    return data.addDepartment;
  },

  async updateDepartment(id, departmentData) {
    const data = await gql(`
      mutation UpdateDepartment($id: Int!, $data: DepartmentInput!) {
        updateDepartment(id: $id, data: $data) { id title description }
      }
    `, { id, data: departmentData });
    return data.updateDepartment;
  },

  async deleteDepartment(id) {
    const data = await gql(`
      mutation DeleteDepartment($id: Int!) {
        deleteDepartment(id: $id)
      }
    `, { id });
    return data.deleteDepartment;
  },

  // --- Users ---
  async getUsers({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetUsers($limit: Int, $offset: Int) {
        users(limit: $limit, offset: $offset) { id username departmentId job time }
      }
    `, { limit, offset });
    return data.users;
  },

  async createUser(userData) {
    const data = await gql(`
      mutation CreateUser($data: UserInput!) {
        addUser(userData: $data) { id username departmentId job time }
      }
    `, { data: userData });
    return data.addUser;
  },

  async updateUser(id, userData) {
    const data = await gql(`
      mutation UpdateUser($id: Int!, $data: UserInput!) {
        updateUser(id: $id, data: $data) { id username departmentId job time }
      }
    `, { id, data: userData });
    return data.updateUser;
  },

  async deleteUser(id) {
    const data = await gql(`
      mutation DeleteUser($id: Int!) {
        deleteUser(id: $id)
      }
    `, { id });
    return data.deleteUser;
  },

  // --- Parts ---
  async getParts({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetParts($limit: Int, $offset: Int) {
        parts(limit: $limit, offset: $offset) { id name departmentId }
      }
    `, { limit, offset });
    return data.parts;
  },

  async createPart(partData) {
    const data = await gql(`
      mutation CreatePart($data: PartInput!) {
        addPart(partData: $data) { id name departmentId }
      }
    `, { data: partData });
    return data.addPart;
  },

  async updatePart(id, partData) {
    const data = await gql(`
      mutation UpdatePart($id: Int!, $data: PartInput!) {
        updatePart(id: $id, data: $data) { id name departmentId }
      }
    `, { id, data: partData });
    return data.updatePart;
  },

  async deletePart(id) {
    const data = await gql(`
      mutation DeletePart($id: Int!) {
        deletePart(id: $id)
      }
    `, { id });
    return data.deletePart;
  },

  // --- Defect Categories ---
  async getDefectCategories({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetDefectCategories($limit: Int, $offset: Int) {
        defectCategories(limit: $limit, offset: $offset) { id title departmentId }
      }
    `, { limit, offset });
    return data.defectCategories;
  },

  async createDefectCategory(defectCategoryData) {
    const data = await gql(`
      mutation CreateDefectCategory($data: DefectCategoryInput!) {
        addDefectCategory(defCatData: $data) { id title departmentId }
      }
    `, { data: defectCategoryData });
    return data.addDefectCategory;
  },

  async updateDefectCategory(id, defectCategoryData) {
    const data = await gql(`
      mutation UpdateDefectCategory($id: Int!, $data: DefectCategoryInput!) {
        updateDefectCategory(id: $id, data: $data) { id title departmentId }
      }
    `, { id, data: defectCategoryData });
    return data.updateDefectCategory;
  },

  async deleteDefectCategory(id) {
    const data = await gql(`
      mutation DeleteDefectCategory($id: Int!) {
        deleteDefectCategory(id: $id)
      }
    `, { id });
    return data.deleteDefectCategory;
  },

  // --- Defects ---
  async getDefects({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetDefects($limit: Int, $offset: Int) {
        defects(limit: $limit, offset: $offset) { id title description partId defectCategoryId }
      }
    `, { limit, offset });
    return data.defects;
  },

  async createDefect(defectData) {
    const data = await gql(`
      mutation CreateDefect($data: DefectInput!) {
        addDefect(defectData: $data) { id title description partId defectCategoryId }
      }
    `, { data: defectData });
    return data.addDefect;
  },

  async updateDefect(id, defectData) {
    const data = await gql(`
      mutation UpdateDefect($id: Int!, $data: DefectInput!) {
        updateDefect(id: $id, data: $data) { id title description partId defectCategoryId }
      }
    `, { id, data: defectData });
    return data.updateDefect;
  },

  async deleteDefect(id) {
    const data = await gql(`
      mutation DeleteDefect($id: Int!) {
        deleteDefect(id: $id)
      }
    `, { id });
    return data.deleteDefect;
  },

  // --- Quality ---
  async getQualities({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetQualities($limit: Int, $offset: Int) {
        qualities(limit: $limit, offset: $offset) { id passFail defectCount partId }
      }
    `, { limit, offset });
    return data.qualities;
  },

  async getQualitiesByPart(partId) {
    const data = await gql(`
      query GetQualities {
        qualities { id passFail defectCount partId }
      }
    `);
    return (data.qualities || []).filter(q => q.partId === partId);
  },

  async createQuality(qualityData) {
    const data = await gql(`
      mutation CreateQuality($data: QualityInput!) {
        addQuality(qualityData: $data) { id passFail defectCount partId }
      }
    `, { data: qualityData });
    return data.addQuality;
  },

  async updateQuality(id, qualityData) {
    const data = await gql(`
      mutation UpdateQuality($id: Int!, $data: QualityInput!) {
        updateQuality(id: $id, data: $data) { id passFail defectCount partId }
      }
    `, { id, data: qualityData });
    return data.updateQuality;
  },

  async deleteQuality(id) {
    const data = await gql(`
      mutation DeleteQuality($id: Int!) {
        deleteQuality(id: $id)
      }
    `, { id });
    return data.deleteQuality;
  },

  // --- Work Centers ---
  async getWorkCenters({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetWorkCenters($limit: Int, $offset: Int) {
        workCenters(limit: $limit, offset: $offset) { id name code departmentId }
      }
    `, { limit, offset });
    return data.workCenters;
  },

  async createWorkCenter(workCenterData) {
    const data = await gql(`
      mutation CreateWorkCenter($data: WorkCenterInput!) {
        addWorkCenter(data: $data) { id name code departmentId }
      }
    `, { data: workCenterData });
    return data.addWorkCenter;
  },

  async updateWorkCenter(id, workCenterData) {
    const data = await gql(`
      mutation UpdateWorkCenter($id: Int!, $data: WorkCenterInput!) {
        updateWorkCenter(id: $id, data: $data) { id name code departmentId }
      }
    `, { id, data: workCenterData });
    return data.updateWorkCenter;
  },

  async deleteWorkCenter(id) {
    const data = await gql(`
      mutation DeleteWorkCenter($id: Int!) {
        deleteWorkCenter(id: $id)
      }
    `, { id });
    return data.deleteWorkCenter;
  },

  // --- Work Orders ---
  async getWorkOrders({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetWorkOrders($limit: Int, $offset: Int) {
        workOrders(limit: $limit, offset: $offset) {
          id number status quantity partId departmentId workCenterId
        }
      }
    `, { limit, offset });
    return data.workOrders;
  },

  async createWorkOrder(workOrderData) {
    const data = await gql(`
      mutation CreateWorkOrder($data: WorkOrderInput!) {
        addWorkOrder(data: $data) { id number status quantity partId departmentId workCenterId }
      }
    `, { data: workOrderData });
    return data.addWorkOrder;
  },

  async updateWorkOrder(id, workOrderData) {
    const data = await gql(`
      mutation UpdateWorkOrder($id: Int!, $data: WorkOrderInput!) {
        updateWorkOrder(id: $id, data: $data) { id number status quantity partId departmentId workCenterId }
      }
    `, { id, data: workOrderData });
    return data.updateWorkOrder;
  },

  async deleteWorkOrder(id) {
    const data = await gql(`
      mutation DeleteWorkOrder($id: Int!) {
        deleteWorkOrder(id: $id)
      }
    `, { id });
    return data.deleteWorkOrder;
  },

  // --- Work Order Ops ---
  async getWorkOrderOps({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetWorkOrderOps($limit: Int, $offset: Int) {
        workOrderOps(limit: $limit, offset: $offset) {
          id workOrderId sequence workCenterId status startedAt completedAt
        }
      }
    `, { limit, offset });
    return data.workOrderOps;
  },

  async createWorkOrderOp(opData) {
    const data = await gql(`
      mutation CreateWorkOrderOp($data: WorkOrderOpInput!) {
        addWorkOrderOp(data: $data) {
          id workOrderId sequence workCenterId status startedAt completedAt
        }
      }
    `, { data: opData });
    return data.addWorkOrderOp;
  },

  async updateWorkOrderOp(id, opData) {
    const data = await gql(`
      mutation UpdateWorkOrderOp($id: Int!, $data: WorkOrderOpInput!) {
        updateWorkOrderOp(id: $id, data: $data) {
          id workOrderId sequence workCenterId status startedAt completedAt
        }
      }
    `, { id, data: opData });
    return data.updateWorkOrderOp;
  },

  async deleteWorkOrderOp(id) {
    const data = await gql(`
      mutation DeleteWorkOrderOp($id: Int!) {
        deleteWorkOrderOp(id: $id)
      }
    `, { id });
    return data.deleteWorkOrderOp;
  },

  // --- Routings ---
  async getRoutings({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetRoutings($limit: Int, $offset: Int) {
        routings(limit: $limit, offset: $offset) { id name partId version }
      }
    `, { limit, offset });
    return data.routings;
  },

  async createRouting(routingData) {
    const data = await gql(`
      mutation CreateRouting($data: RoutingInput!) {
        addRouting(data: $data) { id name partId version }
      }
    `, { data: routingData });
    return data.addRouting;
  },

  async updateRouting(id, routingData) {
    const data = await gql(`
      mutation UpdateRouting($id: Int!, $data: RoutingInput!) {
        updateRouting(id: $id, data: $data) { id name partId version }
      }
    `, { id, data: routingData });
    return data.updateRouting;
  },

  async deleteRouting(id) {
    const data = await gql(`
      mutation DeleteRouting($id: Int!) {
        deleteRouting(id: $id)
      }
    `, { id });
    return data.deleteRouting;
  },

  // --- Routing Steps ---
  async getRoutingSteps({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetRoutingSteps($limit: Int, $offset: Int) {
        routingSteps(limit: $limit, offset: $offset) {
          id routingId sequence workCenterId description standardMinutes
        }
      }
    `, { limit, offset });
    return data.routingSteps;
  },

  async createRoutingStep(stepData) {
    const data = await gql(`
      mutation CreateRoutingStep($data: RoutingStepInput!) {
        addRoutingStep(data: $data) { id routingId sequence workCenterId description standardMinutes }
      }
    `, { data: stepData });
    return data.addRoutingStep;
  },

  async updateRoutingStep(id, stepData) {
    const data = await gql(`
      mutation UpdateRoutingStep($id: Int!, $data: RoutingStepInput!) {
        updateRoutingStep(id: $id, data: $data) {
          id routingId sequence workCenterId description standardMinutes
        }
      }
    `, { id, data: stepData });
    return data.updateRoutingStep;
  },

  async deleteRoutingStep(id) {
    const data = await gql(`
      mutation DeleteRoutingStep($id: Int!) {
        deleteRoutingStep(id: $id)
      }
    `, { id });
    return data.deleteRoutingStep;
  },

  // --- BOMs ---
  async getBOMs({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetBOMs($limit: Int, $offset: Int) {
        boms(limit: $limit, offset: $offset) { id partId revision }
      }
    `, { limit, offset });
    return data.boms;
  },

  async createBOM(bomData) {
    const data = await gql(`
      mutation CreateBOM($data: BOMInput!) {
        addBom(data: $data) { id partId revision }
      }
    `, { data: bomData });
    return data.addBom;
  },

  async updateBOM(id, bomData) {
    const data = await gql(`
      mutation UpdateBOM($id: Int!, $data: BOMInput!) {
        updateBom(id: $id, data: $data) { id partId revision }
      }
    `, { id, data: bomData });
    return data.updateBom;
  },

  async deleteBOM(id) {
    const data = await gql(`
      mutation DeleteBOM($id: Int!) {
        deleteBom(id: $id)
      }
    `, { id });
    return data.deleteBom;
  },

  // --- BOM Items ---
  async getBOMItems({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetBOMItems($limit: Int, $offset: Int) {
        bomItems(limit: $limit, offset: $offset) { id bomId componentPartId quantity }
      }
    `, { limit, offset });
    return data.bomItems;
  },

  async createBOMItem(itemData) {
    const data = await gql(`
      mutation CreateBOMItem($data: BOMItemInput!) {
        addBomItem(data: $data) { id bomId componentPartId quantity }
      }
    `, { data: itemData });
    return data.addBomItem;
  },

  async updateBOMItem(id, itemData) {
    const data = await gql(`
      mutation UpdateBOMItem($id: Int!, $data: BOMItemInput!) {
        updateBomItem(id: $id, data: $data) { id bomId componentPartId quantity }
      }
    `, { id, data: itemData });
    return data.updateBomItem;
  },

  async deleteBOMItem(id) {
    const data = await gql(`
      mutation DeleteBOMItem($id: Int!) {
        deleteBomItem(id: $id)
      }
    `, { id });
    return data.deleteBomItem;
  },

  // --- Activity Logs ---
  async getActivityLogs({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetActivityLogs($limit: Int, $offset: Int) {
        activityLogs(limit: $limit, offset: $offset) {
          id userId partId departmentId workOrderId eventType message createdAt
        }
      }
    `, { limit, offset });
    return data.activityLogs;
  },

  async createActivityLog(logData) {
    const data = await gql(`
      mutation CreateActivityLog($data: ActivityLogInput!) {
        addActivityLog(data: $data) {
          id userId partId departmentId workOrderId eventType message createdAt
        }
      }
    `, { data: logData });
    return data.addActivityLog;
  },

  // --- Floors ---
  async getFloors({ limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetFloors($limit: Int, $offset: Int) {
        floors(limit: $limit, offset: $offset) { id name description }
      }
    `, { limit, offset });
    return data.floors;
  },

  async createFloor(floorData) {
    const data = await gql(`
      mutation CreateFloor($data: FloorInput!) {
        addFloor(data: $data) { id name description }
      }
    `, { data: floorData });
    return data.addFloor;
  },

  async updateFloor(id, floorData) {
    const data = await gql(`
      mutation UpdateFloor($id: Int!, $data: FloorInput!) {
        updateFloor(id: $id, data: $data) { id name description }
      }
    `, { id, data: floorData });
    return data.updateFloor;
  },

  async deleteFloor(id) {
    const data = await gql(`
      mutation DeleteFloor($id: Int!) {
        deleteFloor(id: $id)
      }
    `, { id });
    return data.deleteFloor;
  },

  // --- Floor Zones ---
  async getFloorZones({ floorId = null, limit = 50, offset = 0 } = {}) {
    const data = await gql(`
      query GetFloorZones($floorId: Int, $limit: Int, $offset: Int) {
        floorZones(floorId: $floorId, limit: $limit, offset: $offset) {
          id floorId name zoneType departmentId workCenterId polygon
        }
      }
    `, { floorId, limit, offset });
    return data.floorZones;
  },

  async createFloorZone(zoneData) {
    const data = await gql(`
      mutation CreateFloorZone($data: FloorZoneInput!) {
        addFloorZone(data: $data) { id floorId name zoneType departmentId workCenterId polygon }
      }
    `, { data: zoneData });
    return data.addFloorZone;
  },

  async updateFloorZone(id, zoneData) {
    const data = await gql(`
      mutation UpdateFloorZone($id: Int!, $data: FloorZoneInput!) {
        updateFloorZone(id: $id, data: $data) { id floorId name zoneType departmentId workCenterId polygon }
      }
    `, { id, data: zoneData });
    return data.updateFloorZone;
  },

  async deleteFloorZone(id) {
    const data = await gql(`
      mutation DeleteFloorZone($id: Int!) {
        deleteFloorZone(id: $id)
      }
    `, { id });
    return data.deleteFloorZone;
  },

  // --- Dashboard aggregate ---
  async getShopFloorData() {
    const data = await gql(`
      query DashboardData {
        departments { id title description }
        workCenters { id name code departmentId }
        parts { id name departmentId }
      }
    `);
    return {
      departments: data.departments ?? [],
      workCenters: data.workCenters ?? [],
      parts: data.parts ?? [],
    };
  },
};

export default shopFloorService;
