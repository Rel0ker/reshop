import { createRouter, createWebHistory } from "vue-router";
import { useAuth } from "./store";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
    path: '/success/:id',
    name: 'OrderSuccessWithId',
    component: () => import('./pages/OrderSuccess.vue'),
    props: true,
  },
  {
      path: "/",
      component: () => import("./pages/Home.vue"),
    },
    {
      path: "/login",
      component: () => import("./pages/Login.vue"),
    },
    {
      path: "/register",
      redirect: "/register/buyer",
    },
    {
      path: "/register/buyer",
      component: () => import("./pages/RegisterBuyer.vue"),
    },
    {
      path: "/register/seller",
      component: () => import("./pages/RegisterSeller.vue"),
    },
    {
      path: "/buyer",
      component: () => import("./pages/BuyerDashboard.vue"),
      meta: { requiresAuth: true, role: "buyer" },
    },
    {
      path: "/seller",
      component: () => import("./pages/SellerDashboard.vue"),
      meta: { requiresAuth: true, role: "seller" },
    },
    {
      path: "/popular",
      component: () => import("./pages/PopularProducts.vue"),
    },
    {
      path: "/favorites",
      name: "Favorites",
      component: () => import('./pages/Favorites.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/order-success', // Keep this for backward compatibility if needed, or remove if not used
    name: 'OrderSuccess',
    component: () => import('./pages/OrderSuccess.vue'),
  },
  {
    path: "/product/:id",
    name: "ProductDetail",
    component: () => import("./pages/ProductDetail.vue"),
    props: true,
  },
],
});

router.beforeEach(async (to, from, next) => {
  console.log("Проверка маршрута:", to.path);
  const auth = useAuth();
  
  // Проверяем, требует ли маршрут аутентификации
  if (to.meta.requiresAuth) {
    console.log("Маршрут требует аутентификации");
    console.log("Текущее состояние auth:", {
      token: auth.token,
      role: auth.role,
      userId: auth.userId
    });
    
    if (!auth.token) {
      console.log("Нет токена, перенаправление на /login");
      next("/login");
      return;
    }
    
    const requiredRole = to.meta.role;
    if (requiredRole && auth.role !== requiredRole) {
      console.log("Роль не совпадает, перенаправление на /login");
      next("/login");
      return;
    }
  }
  
  console.log("Разрешаем переход на:", to.path);
  next();
});

export default router;
