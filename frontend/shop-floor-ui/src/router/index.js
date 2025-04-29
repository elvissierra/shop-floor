import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ShopFloorView from '../views/ShopFloorView.vue';

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
      component: ShopFloorView
    },
    {
      path: '/parts',
      name: 'parts',
      component: ShopFloorView
    }
  ]
});

export default router; 