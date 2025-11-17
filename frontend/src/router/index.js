import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
const DepartmentList = () => import('../components/DepartmentList.vue')
const PartList = () => import('../components/PartList.vue')

const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { title: 'Dashboard', breadcrumb: [] } },
  { path: '/departments', name: 'departments', component: DepartmentList, meta: { title: 'Departments', breadcrumb: [{ label: 'Departments' }] } },
  { path: '/parts', name: 'parts', component: PartList, meta: { title: 'Parts', breadcrumb: [{ label: 'Parts' }] } },
  { path: '/shopfloor', name: 'shopfloor', component: () => import('../views/ShopFloorView.vue'), meta: { title: 'Shop Floor', breadcrumb: [{ label: 'Shop Floor' }] }
},
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