<template>
  <div class="group relative bg-white dark:bg-slate-800 rounded-3xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-500 border border-gray-100 dark:border-slate-700 overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5 group-hover:opacity-15 transition-opacity duration-500">
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-br from-tertiary-400 to-primary-400 rounded-full blur-2xl"></div>
    </div>
    
    <!-- Header -->
    <div class="relative mb-8">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-2xl font-bold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300">
          {{ title }}
        </h3>
        <div class="flex items-center space-x-2">
          <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-sm text-gray-500 dark:text-gray-400">{{ period }}</span>
        </div>
      </div>
      
      <!-- Total Value -->
      <div class="flex items-baseline space-x-2">
        <span class="text-3xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
          {{ totalValue }}
        </span>
        <span class="text-sm text-gray-500 dark:text-gray-400">{{ currency }}</span>
      </div>
      
      <!-- Growth Indicator -->
      <div class="flex items-center mt-2">
        <div class="flex items-center space-x-1" :class="growth >= 0 ? 'text-green-600' : 'text-red-600'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="growth >= 0" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path>
          </svg>
          <span class="text-sm font-semibold">{{ Math.abs(growth) }}%</span>
        </div>
        <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">с прошлого периода</span>
      </div>
    </div>
    
    <!-- Chart Container -->
    <div class="relative h-32 mb-6">
      <!-- Chart Bars -->
      <div class="flex items-end justify-between h-full space-x-2">
        <div 
          v-for="(value, index) in chartData" 
          :key="index"
          class="relative flex-1 bg-gradient-to-t from-primary-500 to-secondary-500 rounded-t-lg transition-all duration-500 hover:scale-105"
          :style="{ 
            height: `${(value / Math.max(...chartData)) * 100}%`,
            animationDelay: `${index * 100}ms`
          }"
        >
          <!-- Hover Tooltip -->
          <div class="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
            {{ value }}{{ currency }}
          </div>
        </div>
      </div>
      
      <!-- Chart Labels -->
      <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-2">
        <span v-for="(label, index) in chartLabels" :key="index">{{ label }}</span>
      </div>
    </div>
    
    <!-- Additional Stats -->
    <div class="grid grid-cols-2 gap-4">
      <div class="text-center p-4 bg-gray-50 dark:bg-slate-700 rounded-2xl">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ averageValue }}</div>
        <div class="text-xs text-gray-500 dark:text-gray-400">Среднее</div>
      </div>
      <div class="text-center p-4 bg-gray-50 dark:bg-slate-700 rounded-2xl">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ peakValue }}</div>
        <div class="text-xs text-gray-500 dark:text-gray-400">Пик</div>
      </div>
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
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string;
  totalValue: string | number;
  currency: string;
  growth: number;
  period: string;
  chartData: number[];
  chartLabels: string[];
  averageValue: string | number;
  peakValue: string | number;
}

defineProps<Props>();
</script>

<style scoped>
/* Chart animation */
@keyframes chartBar {
  from { height: 0; }
  to { height: var(--chart-height); }
}

/* Smooth transitions */
.group:hover .group-hover\:-translate-y-2 {
  transform: translateY(-0.5rem);
}

/* Enhanced shadow on hover */
.group:hover .hover\:shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Chart bars animation */
.flex-1 {
  animation: chartBar 1s ease-out forwards;
  animation-fill-mode: both;
}
</style>
