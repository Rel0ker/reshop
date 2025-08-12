<script setup lang="ts">
import { ref } from "vue";
import { api } from "../api";
import { useRouter } from "vue-router";

const email = ref("");
const username = ref("");
const password = ref("");
const passwordConfirm = ref("");
const inn = ref("");
const phoneNumber = ref("");
const legalEntityName = ref("");
const showPassword = ref(false);
const showPasswordConfirm = ref(false);
const router = useRouter();

const toggleShowPassword = () => {
  showPassword.value = !showPassword.value;
};

const toggleShowPasswordConfirm = () => {
  showPasswordConfirm.value = !showPasswordConfirm.value;
};

const submit = async () => {
  try {
    if (password.value !== passwordConfirm.value) {
      alert("Пароли не совпадают!");
      return;
    }
    const { data } = await api.post("/auth/register/", {
      email: email.value,
      username: username.value || email.value,
      password: password.value,
      role: "seller", // Hardcoded for seller
      inn: inn.value,
      phone_number: phoneNumber.value,
      legal_entity_name: legalEntityName.value,
    });
    console.log("Регистрация успешна:", data);
    router.push("/login");
  } catch (error: any) {
    console.error("Ошибка регистрации:", error);
    if (error.response?.data) {
      alert(Object.values(error.response.data).join("\n"));
    } else {
      alert("Ошибка при регистрации");
    }
  }
};
</script>

<template>
  <div class="relative min-h-screen bg-black text-white overflow-hidden flex items-center justify-center">
    <div class="absolute top-0 z-0">
      <div class="bg-[#5900AC] w-[700px] h-[200px] blur-[99px]"></div>
    </div>

    <div class="relative z-20 -mt-16 flex flex-col items-center justify-center w-full min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div
        class="max-w-2xl w-full p-8 rounded-2xl shadow-lg  bg-zinc-900 bg-opacity-90"
      >
      <h1 class="text-center mb-5 text-4xl z-[5]">Регистрация продавца</h1>
        <form class="space-y-6" @submit.prevent="submit">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="email" class="sr-only">Почта</label>
              <input
                id="email"
                v-model="email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="appearance-none relative block w-full px-4 py-3  placeholder-gray-500 text-white bg-[#262525] rounded-xl focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-base"
                placeholder="Почта"
              />
            </div>
            <div>
              <label for="login" class="sr-only">Логин</label>
              <input
                id="login"
                v-model="username"
                name="login"
                type="text"
                autocomplete="username"
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
                  autocomplete="new-password"
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
            <div>
              <label for="password_confirm" class="sr-only">Пароль</label>
              <div class="relative">
                <input
                  id="password_confirm"
                  v-model="passwordConfirm"
                  name="password_confirm"
                  :type="showPasswordConfirm ? 'text' : 'password'"
                  autocomplete="new-password"
                  required
                  class="appearance-none relative block w-full px-4 py-3  placeholder-gray-500 text-white bg-[#262525] rounded-xl focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-base pr-10"
                  placeholder="Пароль еще раз"
                />
                <button
                  type="button"
                  @click="toggleShowPasswordConfirm"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white"
                >
                  <svg
                    v-if="showPasswordConfirm"
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
            <div>
              <label for="inn" class="sr-only">ИНН</label>
              <input
                id="inn"
                v-model="inn"
                name="inn"
                type="text"
                required
                class="appearance-none relative block w-full px-4 py-3  placeholder-gray-500 text-white bg-[#262525] rounded-xl focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-base"
                placeholder="ИНН"
              />
            </div>
            <div>
              <label for="phone_number" class="sr-only">Номер телефона</label>
              <input
                id="phone_number"
                v-model="phoneNumber"
                name="phone_number"
                type="tel"
                required
                class="appearance-none relative block w-full px-4 py-3  placeholder-gray-500 text-white bg-[#262525] rounded-xl focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-base"
                placeholder="Номер телефона"
              />
            </div>
            <div>
              <label for="legal_entity_name" class="sr-only">Название юридического лица</label>
              <input
                id="legal_entity_name"
                v-model="legalEntityName"
                name="legal_entity_name"
                type="text"
                required
                class="appearance-none relative block w-full px-4 py-3  placeholder-gray-500 text-white bg-[#262525] rounded-xl focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-base"
                placeholder="Название юридического лица"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              class="group relative mx-auto flex justify-center py-1 px-14 border border-transparent text-lg font-medium rounded-full text-white bg-gradient-to-r from-[#5900AC] to-[#5900AC] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors duration-300 shadow-lg"
            >
              Присоединиться
            </button>
          </div>

          <div class="text-center text-sm text-gray-400">
            Уже есть аккаунт?
            <router-link to="/login" class="text-[#FFF] p-2 px-4 hover:bg-[#5900AC]/70 rounded-2xl "
              >Войти</router-link
            >
          </div>

          <div class="text-center text-sm text-gray-400">
            Вы покупатель?
            <router-link to="/register/buyer" class="text-[#FFF] p-2 px-4 hover:bg-[#5900AC]/70 rounded-2xl "
              >Регистрация Покупателя</router-link
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template> 