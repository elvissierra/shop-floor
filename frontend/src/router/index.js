import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ShopFloorView from '../views/ShopFloorView.vue';
import DepartmentList from '../components/DepartmentList.vue';
import PartList from '../components/PartList.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/departments',
      name: 'departments',
      component: DepartmentList
    },
    {
      path: '/parts',
      name: 'parts',
      component: PartList
    }
  ]
});

export default router; 