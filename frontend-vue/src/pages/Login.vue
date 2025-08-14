<script setup lang="ts">
import { ref, nextTick } from "vue";
import { api } from "../api";
import { useAuth } from "../store";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const isSubmitting = ref(false);
const router = useRouter();
const auth = useAuth();

const toggleShowPassword = () => {
  showPassword.value = !showPassword.value;
};

const submit = async () => {
  if (isSubmitting.value) return; // Предотвращаем повторную отправку
  
  try {
    isSubmitting.value = true;
    console.log("Отправка запроса на вход...");
    const { data: loginData } = await api.post("/auth/login/", {
      email: email.value,
      password: password.value,
    });
    console.log("Получен ответ:", loginData);

    // Сначала сохраняем токен
    console.log("Сохраняем токен...");
    auth.login(loginData.access);

    // Ждем обновления состояния
    await nextTick();

    // Получаем информацию о пользователе
    console.log("Получаем информацию о пользователе...");
    const { data: userData } = await api.get("/users/me/");
    console.log("Информация о пользователе:", userData);

    // Обновляем роль пользователя
    console.log("Сохраняем роль пользователя...");
    auth.setRole(userData.role);

    // Ждем обновления состояния
    await nextTick();

    console.log("Текущее состояние auth:", {
      token: auth.token,
      role: auth.role,
      userId: auth.userId,
    });

    // Определяем маршрут на основе роли из ответа API
    const targetRoute = userData.role === "seller" ? "/seller" : "/buyer";
    console.log("Перенаправление на:", targetRoute);

    // Сохраняем маршрут в localStorage для перезагрузки
    localStorage.setItem('reshop_redirect_after_login', targetRoute);
    
    // Принудительно перезагружаем страницу
    console.log("Принудительная перезагрузка страницы...");
    window.location.reload();
    
  } catch (error: any) {
    console.error("Ошибка авторизации:", error);
    if (error.response?.data) {
      console.error("Данные ошибки:", error.response.data);
      alert(Object.values(error.response.data).join('\n'));
    } else {
      alert("Неверный email или пароль");
    }
  } finally {
    isSubmitting.value = false;
  }
};


</script>

<style scoped>
/* Анимации для плавающих частиц */
@keyframes particle-float {
  0%, 100% { transform: translateY(0px) translateX(0px); }
  25% { transform: translateY(-20px) translateX(10px); }
  50% { transform: translateY(-10px) translateX(-5px); }
  75% { transform: translateY(-15px) translateX(15px); }
}

.animate-particle-float {
  animation: particle-float 4s ease-in-out infinite;
}

/* Анимация для появления элементов */
@keyframes slide-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-in-up {
  animation: slide-in-up 0.6s ease-out;
}
</style>

<template>
  <div class="relative min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden flex items-center justify-center">
    <!-- Анимированный фон -->
    <div class="absolute inset-0 overflow-hidden">
      <!-- Плавающие частицы -->
      <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-purple-400 rounded-full animate-particle-float" style="animation-delay: 0s;"></div>
      <div class="absolute top-3/4 right-1/4 w-3 h-3 bg-pink-400 rounded-full animate-particle-float" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-2 h-2 bg-blue-400 rounded-full animate-particle-float" style="animation-delay: 2s;"></div>
      <div class="absolute top-1/2 right-1/3 w-1.5 h-1.5 bg-purple-300 rounded-full animate-particle-float" style="animation-delay: 3s;"></div>
    </div>

    <div class="relative z-20 flex flex-col items-center justify-center w-full min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <!-- Форма входа -->
      <div class="max-w-md w-full">
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl shadow-2xl p-8">
          <div class="mb-8 text-center">
            <h2 class="text-3xl font-bold text-white mb-2">
              Добро пожаловать
            </h2>
            <p class="text-gray-400">
              Войдите в свой аккаунт
            </p>
          </div>

          <form class="space-y-6" @submit.prevent="submit">
            <div class="space-y-4">
              <div>
                <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
                  Email
                </label>
                <div class="relative">
                  <input
                    id="email"
                    v-model="email"
                    name="email"
                    type="email"
                    autocomplete="email"
                    required
                    class="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                    placeholder="your@email.com"
                  />
                  <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                    </svg>
                  </div>
                </div>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
                  Пароль
                </label>
                <div class="relative">
                  <input
                    id="password"
                    v-model="password"
                    name="password"
                    :type="showPassword ? 'text' : 'password'"
                    autocomplete="current-password"
                    required
                    class="w-full px-4 py-3 pr-12 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                    placeholder="Введите пароль"
                  />
                  <button
                    type="button"
                    @click="toggleShowPassword"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white transition-colors duration-200"
                  >
                    <svg
                      v-if="showPassword"
                      class="h-5 w-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13.875 18.25V21a1 1 0 01-1 1h-1.75a1 1 0 01-1-1v-2.75m-6.5-6.5V3a1 1 0 011-1h2.75a1 1 0 011 1v2.75m6.5 6.5V21a1 1 0 001 1h1.75a1 1 0 001-1v-2.75m-6.5-6.5V3a1 1 0 001-1h1.75a1 1 0 001 1v2.75m-6.5-6.5H3a1 1 0 01-1-1v-1.75a1 1 0 011-1h2.75m6.5 6.5H21a1 1 0 001-1v-1.75a1 1 0 00-1-1h-2.75m-6.5-6.5H3a1 1 0 00-1-1v-1.75a1 1 0 001-1h2.75m6.5 6.5H21a1 1 0 01-1-1v-1.75a1 1 0 011-1h2.75"
                      />
                    </svg>
                    <svg
                      v-else
                      class="h-5 w-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <div>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-6 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-800 transition-all duration-300 transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                <span v-if="!isSubmitting" class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 5v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                  Войти
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Входим...
                </span>
              </button>
            </div>

            <div class="text-center">
              <p class="text-gray-400 text-sm">
                Еще нет аккаунта?
                <router-link 
                  to="/register" 
                  class="text-purple-400 hover:text-purple-300 font-medium transition-colors duration-200 hover:underline"
                >
                  Присоединиться
                </router-link>
              </p>
            </div>
          </form>
        </div>

        <!-- Кнопка регистрации для продавцов -->
        <div class="mt-6">
          <router-link
            to="/register/seller"
            class="block w-full bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 hover:border-purple-500/50 text-white font-medium py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg flex items-center justify-between group"
          >
            <span class="text-gray-300 group-hover:text-white transition-colors duration-200">
              Регистрация для продавцов
            </span>
            <div class="w-8 h-8 rounded-full flex items-center justify-center bg-purple-600 group-hover:bg-purple-500 transition-colors duration-200">
              <svg
                class="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4.5 19.5l15-15M15 4.5h5.5v5.5"
                />
              </svg>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
