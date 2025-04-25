import { createRouter, createWebHistory } from 'vue-router';
import ShopFloorView from '../views/ShopFloorView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ShopFloorView
    }
  ]
});

export default router; 