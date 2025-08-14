<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";
import LoadingScreen from "./components/LoadingScreen.vue";

// Состояние загрузки
const isLoading = ref(true);
const loadingProgress = ref(0);
const loadingText = ref('Инициализация приложения');

onMounted(async () => {
  // Имитируем процесс загрузки
  const steps = [
    'Инициализация приложения',
    'Загрузка Vue компонентов',
    'Инициализация маршрутизатора',
    'Подключение к API',
    'Загрузка пользовательских данных',
    'Готово!'
  ];
  
  for (let i = 0; i < steps.length; i++) {
    loadingText.value = steps[i];
    loadingProgress.value = (i / (steps.length - 1)) * 100;
    
    if (i < steps.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 800));
    }
  }
  
  // Завершаем загрузку
  setTimeout(() => {
    isLoading.value = false;
  }, 500);
});
</script>

<template>
  <!-- Экран загрузки -->
  <LoadingScreen 
    v-if="isLoading"
    :loading-text="loadingText"
    :show-progress="true"
  />
  
  <!-- Основное приложение -->
  <div v-else class="min-h-screen flex flex-col bg-black animate-fade-in">
    <Navbar class="fixed top-0 left-0 w-full z-50" />
    <main class="flex-grow">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Анимации для плавного появления */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}

/* Дополнительные анимации для LoadingScreen */
@keyframes slideInUp {
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
  animation: slideInUp 0.6s ease-out forwards;
}
</style>



