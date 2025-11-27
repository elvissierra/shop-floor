import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
const DepartmentList = () => import('../components/DepartmentList.vue')
const DepartmentDetailView = () => import('../views/DepartmentDetail.vue')
const PartList = () => import('../components/PartList.vue')
const PartDetailView = () => import('../views/PartDetailView.vue')

const WorkCentersPage = () => import('../views/WorkCentersPage.vue')
const WorkCenterDetailView = () => import('../views/WorkCenterDetailView.vue')
const FloorMapView = () => import('../views/FloorMapView.vue')

const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { title: 'Dashboard', breadcrumb: [] } },
  { path: '/departments', name: 'departments', component: DepartmentList, meta: { title: 'Departments', breadcrumb: [{ label: 'Departments' }] } },
  {
    path: '/departments/:id',
    name: 'department-detail',
    component: DepartmentDetailView,
    props: true,
    meta: {
      title: 'Department',
      breadcrumb: [
        { label: 'Departments', to: { name: 'departments' } },
        { label: 'Detail' },
      ],
    },
  },
  { path: '/parts', name: 'parts', component: PartList, meta: { title: 'Parts', breadcrumb: [{ label: 'Parts' }] } },
  {
    path: '/parts/:id',
    name: 'part-detail',
    component: PartDetailView,
    props: true,
    meta: {
      title: 'Part',
      breadcrumb: [
        { label: 'Parts', to: { name: 'parts' } },
        { label: 'Detail' },
      ],
    },
  },
  {
    path: '/work-centers',
    name: 'work-centers',
    component: WorkCentersPage,
    meta: { title: 'Work Centers', breadcrumb: [{ label: 'Work Centers' }] }
  },
  {
    path: '/work-centers/:id',
    name: 'work-center-detail',
    component: WorkCenterDetailView,
    props: true,
    meta: { title: 'Work Center', breadcrumb: [{ label: 'Work Centers' }, { label: 'Detail' }] }
  },
  { path: '/shopfloor', name: 'shopfloor', component: () => import('../views/ShopFloorView.vue'), meta: { title: 'Shop Floor', breadcrumb: [{ label: 'Shop Floor' }] } },
  {
    path: '/floor-map',
    name: 'floor-map',
    component: FloorMapView,
    meta: { title: 'Shop Floor Layout', breadcrumb: [{ label: 'Shop Floor Layout' }] }
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