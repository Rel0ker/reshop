<script setup lang="ts">
import { ref } from "vue";
import { api } from "../api";
import { useRouter } from "vue-router";

const email = ref("");
const username = ref("");
const password = ref("");
const passwordConfirm = ref("");
const showPassword = ref(false);
const showPasswordConfirm = ref(false);
const isSubmitting = ref(false);
const router = useRouter();

const toggleShowPassword = () => {
  showPassword.value = !showPassword.value;
};

const toggleShowPasswordConfirm = () => {
  showPasswordConfirm.value = !showPasswordConfirm.value;
};

const submit = async () => {
  if (isSubmitting.value) return; // Предотвращаем повторную отправку
  
  try {
    if (password.value !== passwordConfirm.value) {
      alert("Пароли не совпадают!");
      return;
    }
    
    isSubmitting.value = true;
    const { data } = await api.post("/auth/register/", {
      email: email.value,
      username: username.value || email.value,
      password: password.value,
      role: "buyer", // Hardcoded for buyer
    });
    console.log("Регистрация успешна:", data);
    
    // Показываем сообщение об успешной регистрации
    alert("Регистрация успешна! Теперь вы можете войти в систему.");
    
    // Перенаправляем на страницу входа
    router.push("/login");
  } catch (error: any) {
    console.error("Ошибка регистрации:", error);
    if (error.response?.data) {
      alert(Object.values(error.response.data).join("\n"));
    } else {
      alert("Ошибка при регистрации");
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
      <!-- Форма регистрации -->
      <div class="max-w-2xl w-full">
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl shadow-2xl p-8">
          <div class="mb-8 text-center">
            <h2 class="text-3xl font-bold text-white mb-2">
              Регистрация покупателя
            </h2>
            <p class="text-gray-400">
              Создайте аккаунт для покупок
            </p>
          </div>

          <form class="space-y-6" @submit.prevent="submit">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                <label for="login" class="block text-sm font-medium text-gray-300 mb-2">
                  Логин
                </label>
                <div class="relative">
                  <input
                    id="login"
                    v-model="username"
                    name="login"
                    type="text"
                    autocomplete="username"
                    class="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                    placeholder="Ваш логин"
                  />
                  <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
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
                    autocomplete="new-password"
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

              <div>
                <label for="password_confirm" class="block text-sm font-medium text-gray-300 mb-2">
                  Подтвердите пароль
                </label>
                <div class="relative">
                  <input
                    id="password_confirm"
                    v-model="passwordConfirm"
                    name="password_confirm"
                    :type="showPasswordConfirm ? 'text' : 'password'"
                    autocomplete="new-password"
                    required
                    class="w-full px-4 py-3 pr-12 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                    placeholder="Пароль еще раз"
                  />
                  <button
                    type="button"
                    @click="toggleShowPasswordConfirm"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white transition-colors duration-200"
                  >
                    <svg
                      v-if="showPasswordConfirm"
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
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                  Присоединиться
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Регистрируем...
                </span>
              </button>
            </div>

            <div class="space-y-3 text-center">
              <p class="text-gray-400 text-sm">
                Уже есть аккаунт?
                <router-link 
                  to="/login" 
                  class="text-purple-400 hover:text-purple-300 font-medium transition-colors duration-200 hover:underline"
                >
                  Войти
                </router-link>
              </p>

              <p class="text-gray-400 text-sm">
                Вы продавец?
                <router-link 
                  to="/register/seller" 
                  class="text-purple-400 hover:text-purple-300 font-medium transition-colors duration-200 hover:underline"
                >
                  Регистрация продавца
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template> 