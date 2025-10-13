http://localhost:8000/graphql
http://localhost:8000/healthz
http://localhost:8080 (UI)

Browser (user)
   │
   ▼
Vue Router → loads a View (.vue page)
   │
   ▼
View lifecycle (onMounted) triggers store actions
   │
   ▼
Pinia store (shopFloor.js) runs actions
   │
   ▼
services/api.js sends GraphQL POSTs to /graphql
   │
   ▼
Backend resolvers return JSON → store updates state → view re-renders
# Frontend ↔ Backend Workflow (Vue/Vite + Pinia + GraphQL)

This app uses **Vue 3 + Vite** on the frontend and a **GraphQL** backend at `/graphql`. The service layer (`src/services/api.js`) posts GraphQL queries with `fetch` (no extra deps).

## High‑level picture
```
Browser (user)
   │
   ▼
Vue Router → loads a View (.vue page)
   │
   ▼
View lifecycle (onMounted) triggers store actions
   │
   ▼
Pinia store (shopFloor.js) runs actions
   │
   ▼
services/api.js sends GraphQL POSTs to /graphql
   │
   ▼
Backend resolvers return JSON → store updates state → view re-renders
```

## Key files & purpose
- `src/views/HomeView.vue` – Landing page; on mount fetches **Departments** and **Parts** to show simple stats.
- `src/views/ShopFloorView.vue` – Dashboard; on mount calls `store.fetchShopFloorData()` (combined departments + parts for now).
- `src/components/DepartmentList.vue` – Lists departments; supports delete.
- `src/components/PartList.vue` – Lists parts.
- `src/stores/shopFloor.js` – Pinia store (central state, actions, loading/error handling) that calls the service layer.
- `src/services/api.js` – **GraphQL service** using `fetch` to `/graphql`; maps GraphQL camelCase fields (e.g., `departmentId`) to the UI’s snake_case (`department_id`) where needed.

## Lifecycle snapshots (order of events)

### Home page
**Flow:** `HomeView.vue` → `store/shopFloor.js` → `services/api.js` → `/graphql` → Store → `HomeView.vue`
1. Route mounts `HomeView.vue`.
2. `onMounted()` calls `store.fetchDepartments()` and `store.fetchParts()`.
3. Store sets `loading`, calls service (GraphQL queries), updates `error`/state.
4. Service POSTs to `/graphql`, returns JSON data.
5. Store returns arrays; view computes counts and re-renders.

### Departments page (list + delete)
**Flow:** `DepartmentList.vue` → Store → Service → `/graphql` → Store → `DepartmentList.vue`
1. Route mounts `DepartmentList.vue`; it calls `store.fetchDepartments()`.
2. Store queries departments via GraphQL.
3. Delete button calls `store.deleteDepartment(id)` → GraphQL mutation; UI filters out the deleted card.

### Shop Floor dashboard
**Flow:** `ShopFloorView.vue` → Store → Service → `/graphql`
1. Route mounts; `onMounted()` calls `store.fetchShopFloorData()`.
2. Store runs a single GraphQL query for `{ departments, parts }` and stores `{ departments, parts }`.
3. View renders a JSON preview (replace with charts/tiles later).

## Configuration
- **Frontend:** set the backend URL (optional). Defaults to `http://localhost:8000/graphql`.
  ```env
  # frontend/.env.development
  VITE_API_URL=http://localhost:8000/graphql
  ```
- **Backend (reference):** `backend/main.py` serves GraphQL at `/graphql` and enables CORS for `http://localhost:5173`.

## Quick test
```bash
# Backend running on :8000, frontend on :5173
curl -X POST http://localhost:8000/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ departments { id title description } }"}'
```
Then visit `http://localhost:5173/`:
- Home → shows counts for Departments/Parts
- /departments → lists departments
- /parts → lists parts
- /shop-floor → shows combined JSON payload

## Common gotchas
- **CORS:** if browser errors, add your Vite origin to `allow_origins` in `backend/main.py`.
- **Docker networking:** if backend is in Docker and Postgres is on host, use `host.docker.internal` in `DATABASE_URL`; if Postgres is a Compose service (e.g., `db`), use `db` as host.
- **Schema changes:** after changing schema/resolvers, hard-refresh Vite; consider GraphQL Codegen later for typed queries.



<!--
## Next Steps (Roadmap)

1. Bring the DB up & migrate
   - Ensure role/db exist:
     CREATE ROLE shopfloor_user WITH LOGIN PASSWORD 'sf_password';
     CREATE DATABASE shopfloor_db OWNER shopfloor_user;
     ALTER SCHEMA public OWNER TO shopfloor_user;
   - Run from backend/:
     alembic revision --autogenerate -m "initial schema"
     alembic upgrade head

2. Run both apps & sanity-check
   - Backend: uvicorn backend.main:app --reload --port 8000
   - Frontend: npm run dev (with VITE_API_URL=http://localhost:8000/graphql)
   - Visit /, /departments, /parts, /shop-floor

3. Wire basic create flows in the UI
   - Add “Create Department” form → createDepartment mutation
   - Add “Create Part” form → createPart mutation

4. Stabilize environments
   - Keep frontend VITE_API_URL in .env.*
   - Backend .env: adjust host if Dockerized PG

5. Lock CORS & ports
   - Extend allow_origins in backend/main.py for other dev/prod domains

6. Add minimal tests
   - Backend: pytest for GraphQL CRUD
   - Frontend: smoke tests for store actions

7. Nice-to-haves
   - Pagination/filtering in queries
   - UI error surface (toast/banner)
   - Seed script for demo data

8. Container & compose (deployment prep)
   - docker-compose.yml with backend, frontend, db
   - DATABASE_URL uses host db service
-->