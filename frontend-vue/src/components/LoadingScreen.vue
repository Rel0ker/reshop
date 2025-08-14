<template>
  <div class="fixed inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center z-50">
    <!-- Анимированный фон -->
    <div class="absolute inset-0 overflow-hidden">
      <!-- Плавающие частицы -->
      <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-purple-400 rounded-full animate-particle-float" style="animation-delay: 0s;"></div>
      <div class="absolute top-3/4 right-1/4 w-3 h-3 bg-pink-400 rounded-full animate-particle-float" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-2 h-2 bg-blue-400 rounded-full animate-particle-float" style="animation-delay: 2s;"></div>
      <div class="absolute top-1/2 right-1/3 w-1 h-1 bg-cyan-400 rounded-full animate-particle-float" style="animation-delay: 0.5s;"></div>
      
      <!-- Волны -->
      <div class="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-purple-600/20 to-transparent"></div>
    </div>

    <!-- Основной контент загрузки -->
    <div class="relative z-10 text-center animate-slide-in-up max-w-lg mx-auto px-4">
      <!-- Логотип -->
      <div class="mb-8 flex justify-center">
        <div class="relative w-24 h-24">
          <!-- Основной круг логотипа -->
          <div class="w-24 h-24 bg-gradient-to-br from-purple-500 via-pink-500 to-purple-600 rounded-full flex items-center justify-center shadow-2xl animate-pulse">
            <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          
          <!-- Вращающееся кольцо -->
          <div class="absolute inset-0 w-24 h-24 border-4 border-transparent border-t-purple-300 border-r-pink-300 rounded-full animate-spin"></div>
          
          <!-- Пульсирующее кольцо -->
          <div class="absolute inset-0 w-24 h-24 border-2 border-purple-400/30 rounded-full animate-ping"></div>
        </div>
      </div>

      <!-- Название приложения -->
      <h1 class="text-4xl md:text-5xl font-bold text-white mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent animate-pulse">
        Re:shop
      </h1>
      
      <!-- Подзаголовок -->
      <p class="text-lg md:text-xl text-gray-300 mb-8 animate-pulse">
        Цифровая торговая площадка
      </p>


      

      <!-- Текст загрузки -->
      <div class="space-y-2">
        <p class="text-white text-lg font-medium animate-pulse">
          {{ loadingText }}
        </p>
        <p class="text-gray-400 text-sm animate-pulse">
          Пожалуйста, подождите...
        </p>
      </div>

      <!-- Прогресс-бар -->
      <div class="w-64 mx-auto mt-6">
        <div class="w-full bg-purple-200/20 rounded-full h-2 overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all duration-1000 ease-out"
            :style="{ width: progress + '%' }"
          ></div>
        </div>
        <p class="text-purple-300 text-xs mt-2">{{ Math.round(progress) }}%</p>
      </div>
    </div>

    <!-- Нижняя информация -->
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-center text-gray-400 text-sm">
      <p class="animate-pulse">Загрузка компонентов...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface Props {
  loadingText?: string;
  showProgress?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  loadingText: 'Инициализация приложения',
  showProgress: true
});

const progress = ref(0);

onMounted(() => {
  if (props.showProgress) {
    // Симулируем прогресс загрузки
    const interval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += Math.random() * 15;
      } else if (progress.value < 95) {
        progress.value += Math.random() * 3;
      }
    }, 200);

    // Очищаем интервал при размонтировании
    return () => clearInterval(interval);
  }
});
</script>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* Дополнительные анимации для частиц */
@keyframes particle-float {
  0%, 100% { transform: translateY(0px) translateX(0px); }
  25% { transform: translateY(-20px) translateX(10px); }
  50% { transform: translateY(-10px) translateX(-5px); }
  75% { transform: translateY(-15px) translateX(15px); }
}

.animate-particle-float {
  animation: particle-float 4s ease-in-out infinite;
}

/* Улучшенные анимации для колеса загрузки */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Анимация для центральной точки */
@keyframes pulse-center {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

.animate-pulse-center {
  animation: pulse-center 2s ease-in-out infinite;
}
</style>
