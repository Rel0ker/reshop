import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router.ts";
import App from "./App.vue";
import { useAuth } from "./composables/useAuth";
import "./style.css";

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);

// Инициализация аутентификации и монтирование приложения после загрузки данных пользователя
async function initializeApp() {
  const { init } = useAuth();
  
  // Добавляем небольшую задержку для демонстрации загрузки
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  await init();
  app.mount("#app");
}

initializeApp();
