<template>
  <div class="group relative bg-white dark:bg-slate-800 rounded-3xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-500 border border-gray-100 dark:border-slate-700 overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5 group-hover:opacity-15 transition-opacity duration-500">
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-br from-tertiary-400 to-primary-400 rounded-full blur-2xl"></div>
    </div>
    
    <!-- Icon Container -->
    <div class="relative mb-6">
      <div class="w-16 h-16 bg-gradient-to-br from-primary-500 via-secondary-500 to-tertiary-500 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
        <component :is="icon" class="w-8 h-8 text-white" />
      </div>
      <div class="absolute -inset-2 bg-gradient-to-br from-primary-400 via-secondary-400 to-tertiary-400 rounded-2xl blur opacity-0 group-hover:opacity-75 transition-opacity duration-500"></div>
    </div>
    
    <!-- Content -->
    <div class="relative">
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300">
        {{ title }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
        {{ description }}
      </p>
    </div>
    
    <!-- Hover Effect Border -->
    <div class="absolute inset-0 border-2 border-transparent group-hover:border-primary-500/20 rounded-3xl transition-all duration-500 pointer-events-none opacity-0 group-hover:opacity-100"></div>
    
    <!-- Floating Elements -->
    <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-all duration-700 delay-100">
      <div class="w-2 h-2 bg-secondary-400 rounded-full animate-pulse"></div>
    </div>
    <div class="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-all duration-700 delay-200">
      <div class="w-1.5 h-1.5 bg-tertiary-400 rounded-full animate-pulse"></div>
    </div>
    
    <!-- Corner Accent -->
    <div class="absolute top-0 right-0 w-0 h-0 border-l-[50px] border-l-transparent border-t-[50px] border-t-primary-500/10 opacity-0 group-hover:opacity-100 transition-all duration-500 transform rotate-45 translate-x-6 -translate-y-6"></div>
  </div>
</template>

<script setup lang="ts">
import type { Component } from 'vue';

interface Props {
  icon: Component;
  title: string;
  description: string;
}

defineProps<Props>();
</script>

<style scoped>
/* Smooth transitions */
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}

.group:hover .group-hover\:-translate-y-2 {
  transform: translateY(-0.5rem);
}

.group:hover .group-hover\:rotate-6 {
  transform: rotate(6deg);
}

/* Enhanced shadow on hover */
.group:hover .hover\:shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Floating elements animation */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>
