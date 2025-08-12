<template>
  <div class="relative w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 via-gray-200 to-gray-300 dark:from-slate-700 dark:via-slate-600 dark:to-slate-500 overflow-hidden">
    <!-- Animated background pattern -->
    <div class="absolute inset-0 opacity-20">
      <div class="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-0 right-0 w-24 h-24 bg-gradient-to-br from-pink-400 to-red-500 rounded-full blur-2xl animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute top-1/2 left-1/2 w-16 h-16 bg-gradient-to-br from-green-400 to-blue-500 rounded-full blur-xl animate-pulse" style="animation-delay: 2s;"></div>
    </div>
    
    <!-- Main icon -->
    <div class="relative z-10 text-center">
      <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-gray-400 to-gray-600 dark:from-slate-500 dark:to-slate-700 rounded-2xl flex items-center justify-center shadow-lg">
        <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
      </div>
      
      <!-- Text -->
      <div class="text-gray-600 dark:text-gray-300 text-sm font-medium">
        {{ text || 'Изображение отсутствует' }}
      </div>
      
      <!-- Subtitle -->
      <div class="text-gray-500 dark:text-gray-400 text-xs mt-1">
        {{ subtitle || 'Фото не загружено' }}
      </div>
    </div>
    
    <!-- Floating elements -->
    <div class="absolute top-4 left-4 w-3 h-3 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.5s;"></div>
    <div class="absolute top-6 right-6 w-2 h-2 bg-purple-400 rounded-full animate-bounce" style="animation-delay: 1s;"></div>
    <div class="absolute bottom-6 left-6 w-2 h-2 bg-pink-400 rounded-full animate-bounce" style="animation-delay: 1.5s;"></div>
    
    <!-- Corner accent -->
    <div class="absolute top-0 right-0 w-0 h-0 border-l-[30px] border-t-[30px] border-l-transparent border-t-blue-500 opacity-60"></div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  text?: string;
  subtitle?: string;
}

defineProps<Props>();
</script>

<style scoped>
.animate-pulse {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-bounce {
  animation: bounce 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.4;
  }
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -8px, 0);
  }
  70% {
    transform: translate3d(0, -4px, 0);
  }
  90% {
    transform: translate3d(0, -2px, 0);
  }
}
</style>
