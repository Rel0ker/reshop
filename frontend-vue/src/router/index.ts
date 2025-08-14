import { createRouter, createWebHistory } from 'vue-router';
import Home from '../pages/Home.vue';
import Login from '../pages/Login.vue';
import Register from '../pages/Register.vue';
import BuyerDashboard from '../pages/BuyerDashboard.vue';
import SellerDashboard from '../pages/SellerDashboard.vue';
import { useAuth } from '../composables/useAuth';
// Убираю прямой импорт Settings

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
      component: () => import("../pages/Home.vue"),  
    },
    {
      path: "/blog",
      name: "Blog",
      component: () => import("../pages/Home.vue"),  
    },
    {
      path: "/support",
      name: "Support",
      component: () => import("../pages/Home.vue"),  
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
    {
      path: "/success/:id",
      name: "order-success",
      component: () => import("../pages/OrderSuccess.vue"),
      props: true
    },
  ]
});

// Навигационный guard
router.beforeEach((to, from, next) => {
  const { isAuthenticated, user } = useAuth();

  // Проверяем, есть ли сохраненный маршрут для перенаправления после авторизации
  const redirectAfterLogin = localStorage.getItem('reshop_redirect_after_login');
  
  if (redirectAfterLogin && isAuthenticated.value) {
    // Очищаем сохраненный маршрут
    localStorage.removeItem('reshop_redirect_after_login');
    
    // Перенаправляем на сохраненный маршрут
    next(redirectAfterLogin);
    return;
  }

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
    // Если пользователь авторизован и пытается зайти на страницу входа/регистрации,
    // перенаправляем в соответствующий личный кабинет
    if (user.value?.role === "buyer") {
      next('/buyer');
    } else if (user.value?.role === "seller") {
      next('/seller');
    } else {
      next('/');
    }
    return;
  }

  // Если пользователь авторизован и заходит на главную страницу,
  // перенаправляем в соответствующий личный кабинет
  if (to.path === '/' && isAuthenticated.value && user.value?.role) {
    if (user.value.role === "buyer") {
      next('/buyer');
    } else if (user.value.role === "seller") {
      next('/seller');
    } else {
      next();
    }
    return;
  }

  next();
});

export default router;