<script setup lang="ts">
import { ref, nextTick } from "vue";
import { api } from "../api";
import { useAuth } from "../store";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const router = useRouter();
const auth = useAuth();

const toggleShowPassword = () => {
  showPassword.value = !showPassword.value;
};

const submit = async () => {
  try {
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

    // Делаем редирект
    await router.push(targetRoute);
    console.log("Перенаправление выполнено");
  } catch (error: any) {
    console.error("Ошибка авторизации:", error);
    if (error.response?.data) {
      console.error("Данные ошибки:", error.response.data);
      alert(Object.values(error.response.data).join('\n'));
    } else {
      alert("Неверный email или пароль");
    }
  }
};


</script>

<template>
  <div class="relative min-h-screen bg-black text-white overflow-hidden flex items-center justify-center">
<div class="absolute top-0 z-0">
    <div class="bg-[#5900AC] w-[700px] h-[200px] blur-[99px]"></div>
</div>


   

    <div class="relative z-20 -mt-32  flex flex-col items-center justify-center w-full min-h-screen py-12 px-4 sm:px-6 lg:px-8">

      <div
        class="max-w-md w-full p-8 rounded-2xl shadow-lg  bg-zinc-900 bg-opacity-90"
      >
        <div class="mb-8">
          <h2 class="text-center  text-4xl font-extrabold text-white">
            Вход
          </h2>
        </div>
        <form class="space-y-6" @submit.prevent="submit">
          <div class="space-y-4">
            <div>
              <label for="email" class="sr-only">Логин</label>
              <input
                id="email"
                v-model="email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="appearance-none relative block w-full px-4 py-3  placeholder-gray-500 text-white bg-[#262525] rounded-xl focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-base"
                placeholder="Логин"
              />
            </div>
            <div>
              <label for="password" class="sr-only">Пароль</label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  name="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  required
                  class="appearance-none relative block w-full px-4 py-3  placeholder-gray-500 text-white bg-[#262525] rounded-xl focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-base pr-10"
                  placeholder="Пароль"
                />
                <button
                  type="button"
                  @click="toggleShowPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white"
                >
                  <svg
                    v-if="showPassword"
                    class="h-5 w-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13.875 18.25V21a1 1 0 01-1 1h-1.75a1 1 0 01-1-1v-2.75m-6.5-6.5V3a1 1 0 011-1h2.75a1 1 0 011 1v2.75m6.5 6.5V21a1 1 0 001 1h1.75a1 1 0 001-1v-2.75m-6.5-6.5V3a1 1 0 001-1h1.75a1 1 0 001 1v2.75m-6.5 6.5H3a1 1 0 01-1-1v-1.75a1 1 0 011-1h2.75m6.5 6.5H21a1 1 0 001-1v-1.75a1 1 0 00-1-1h-2.75m-6.5-6.5H3a1 1 0 00-1-1v-1.75a1 1 0 001-1h2.75m6.5 6.5H21a1 1 0 01-1-1v-1.75a1 1 0 011-1h-2.75"
                    ></path>
                  </svg>
                  <svg
                    v-else
                    class="h-5 w-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    ></path>
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              class="group relative mx-auto flex justify-center py-1 px-14 border border-transparent text-lg font-medium rounded-full text-white bg-gradient-to-r from-[#5900AC] to-[#5900AC] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors duration-300 shadow-lg"
            >
              Войти
            </button>
          </div>

          <div class="text-center text-sm text-gray-400">
            Еще нет аккаунта?
            <router-link to="/register" class=" text-[#FFF] p-2 px-4 hover:bg-[#5900AC]/70 rounded-2xl "
              >Присоединиться</router-link>
          </div>
        </form>
      </div>

      <!-- Moved and restyled Seller Login Button -->
      <router-link
        to="/register/seller"
        class="block w-full max-w-md mt-4 px-10 py-2 text-white text-lg font-semibold shadow-lg transition-all duration-300 rounded-2xl border border-[#5900AC]/50  bg-zinc-900 bg-opacity-90 flex items-center justify-between"
      >
        <span class="block">Регистрация для продавцов</span>
        <div class="w-8 h-8 rounded-full flex items-center justify-center bg-#5900AC]">
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4.5 19.5l15-15M15 4.5h5.5v5.5"
            ></path>
          </svg>
        </div>
      </router-link>
    </div>
  </div>
</template>
