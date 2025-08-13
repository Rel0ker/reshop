<template>
  <div class="group relative bg-white dark:bg-slate-800 rounded-3xl p-6 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-500 border border-gray-100 dark:border-slate-700 overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5 group-hover:opacity-10 transition-opacity duration-500">
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-br from-tertiary-400 to-primary-400 rounded-full blur-2xl"></div>
    </div>
    
    <!-- Icon Container -->
    <div class="relative mb-6">
      <div class="w-16 h-16 bg-gradient-to-br from-primary-500 via-secondary-500 to-tertiary-500 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-500">
        <component :is="icon" class="w-8 h-8 text-white" />
      </div>
      <div class="absolute -inset-2 bg-gradient-to-br from-primary-400 via-secondary-400 to-tertiary-400 rounded-2xl blur opacity-0 group-hover:opacity-75 transition-opacity duration-500"></div>
    </div>
    
    <!-- Content -->
    <div class="relative">
      <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300">
        {{ value }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 font-medium mb-3">
        {{ title }}
      </p>
      <p class="text-sm text-gray-500 dark:text-gray-500">
        {{ description }}
      </p>
    </div>
    
    <!-- Progress Bar (if applicable) -->
    <div v-if="progress !== undefined" class="relative mt-4">
      <div class="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
        <div 
          class="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-1000 ease-out"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>
      <span class="text-xs text-gray-500 dark:text-gray-400 mt-1 block">{{ progress }}%</span>
    </div>
    
    <!-- Hover Effect -->
    <div class="absolute inset-0 border-2 border-transparent group-hover:border-primary-500/20 rounded-3xl transition-all duration-500 pointer-events-none opacity-0 group-hover:opacity-100"></div>
  </div>
</template>

<script setup lang="ts">
import type { Component } from 'vue';

interface Props {
  icon: Component;
  title: string;
  value: string | number;
  description: string;
  progress?: number;
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

/* Enhanced shadow on hover */
.group:hover .hover\:shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
</style>
