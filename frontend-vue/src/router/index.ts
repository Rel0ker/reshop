import { createRouter, createWebHistory } from 'vue-router';
import Home from '../pages/Home.vue';
import Login from '../pages/Login.vue';
import Register from '../pages/Register.vue';
import BuyerDashboard from '../pages/BuyerDashboard.vue';
import SellerDashboard from '../pages/SellerDashboard.vue';
import { useAuth } from '../composables/useAuth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresGuest: true }
    },
    {
      path: '/buyer',
      name: 'buyer',
      component: BuyerDashboard,
      meta: { requiresAuth: true, role: 'buyer' }
    },
    {
      path: '/seller',
      name: 'seller',
      component: SellerDashboard,
      meta: { requiresAuth: true, role: 'seller' }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../pages/Settings.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/search',
      name: 'search',
      component: () => import("../pages/Search.vue"),
    },
    {
      path: "/security",
      name: "Security",
      component: () => import("../pages/Home.vue"), // Placeholder, replace with actual component
    },
    {
      path: "/blog",
      name: "Blog",
      component: () => import("../pages/Home.vue"), // Placeholder, replace with actual component
    },
    {
      path: "/support",
      name: "Support",
      component: () => import("../pages/Home.vue"), // Placeholder, replace with actual component
    },
    {
      path: "/popular",
      name: "popular",
      component: () => import("../pages/PopularProducts.vue"),
    },
    {
      path: "/product/:id",
      name: "product-detail",
      component: () => import("../pages/ProductDetail.vue"),
    },
    {
      path: "/test-search",
      name: "test-search",
      component: () => import("../pages/TestSearch.vue"),
    },
  ]
});

// Навигационный guard
router.beforeEach((to, from, next) => {
  const { isAuthenticated, user } = useAuth();

  // Если маршрут требует аутентификации
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login');
    return;
  }

  // Если маршрут требует определенной роли
  if (to.meta.role && user.value?.role !== to.meta.role) {
    next('/');
    return;
  }

  // Если маршрут только для гостей
  if (to.meta.requiresGuest && isAuthenticated.value) {
    next('/');
    return;
  }

  next();
});

export default router;