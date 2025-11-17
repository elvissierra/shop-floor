import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import DepartmentList from '../components/DepartmentList.vue';
import PartList from '../components/PartList.vue';

const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { title: 'Dashboard', breadcrumb: [] } },
  { path: '/departments', name: 'departments', component: DepartmentList, meta: { title: 'Departments', breadcrumb: [{ label: 'Departments' }] } },
  { path: '/parts', name: 'parts', component: PartList, meta: { title: 'Parts', breadcrumb: [{ label: 'Parts' }] } },
  { path: '/shopfloor', name: 'shopfloor', component: () => import('../views/ShopFloorView.vue'),},
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() { return { top: 0 }; },
});

router.afterEach((to) => {
  const base = 'Shop Floor Management';
  document.title = to.meta?.title ? `${to.meta.title} • ${base}` : base;
});

export default router;