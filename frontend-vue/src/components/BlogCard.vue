<template>
  <div class="group relative bg-white dark:bg-slate-800 rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 border border-gray-100 dark:border-slate-700">
    <!-- Image Container -->
    <div class="relative h-48 overflow-hidden">
      <img 
        :src="image" 
        :alt="title"
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      
      <!-- Category Badge -->
      <div class="absolute top-4 left-4">
        <span class="px-3 py-1.5 bg-gradient-to-r from-primary-500 to-secondary-500 text-white text-xs font-semibold rounded-full shadow-lg">
          {{ category }}
        </span>
      </div>
      
      <!-- Date Badge -->
      <div class="absolute top-4 right-4">
        <div class="px-3 py-1.5 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm text-gray-900 dark:text-white text-xs font-semibold rounded-full shadow-lg">
          {{ formatDate(date) }}
        </div>
      </div>
      
      <!-- Hover Overlay -->
      <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex items-center justify-center">
        <div class="bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm px-6 py-3 rounded-2xl shadow-xl transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
          <span class="text-gray-900 dark:text-white font-semibold">Читать далее</span>
        </div>
      </div>
    </div>
    
    <!-- Content -->
    <div class="p-6">
      <div class="flex items-center space-x-2 mb-3">
        <div class="w-2 h-2 bg-primary-500 rounded-full"></div>
        <span class="text-xs text-gray-500 dark:text-gray-400">{{ readTime }} мин чтения</span>
      </div>
      
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300 line-clamp-2">
        {{ title }}
      </h3>
      
      <p class="text-gray-600 dark:text-gray-400 mb-4 leading-relaxed line-clamp-3">
        {{ excerpt }}
      </p>
      
      <!-- Author Info -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="relative">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 via-secondary-500 to-tertiary-500 rounded-full flex items-center justify-center shadow-lg">
              <span class="text-white font-bold text-sm">
                {{ authorInitial }}
              </span>
            </div>
            <div class="absolute -inset-1 bg-gradient-to-br from-primary-400 via-secondary-400 to-tertiary-400 rounded-full blur opacity-0 group-hover:opacity-75 transition-opacity duration-500"></div>
          </div>
          <div>
            <p class="font-semibold text-gray-900 dark:text-white text-sm">{{ authorName }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ authorRole }}</p>
          </div>
        </div>
        
        <!-- Action Button -->
        <div class="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-300">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
          </svg>
        </div>
      </div>
    </div>
    
    <!-- Hover Effect Border -->
    <div class="absolute inset-0 border-2 border-transparent group-hover:border-primary-500/20 rounded-3xl transition-all duration-500 pointer-events-none opacity-0 group-hover:opacity-100"></div>
    
    <!-- Corner Accent -->
    <div class="absolute top-0 right-0 w-0 h-0 border-l-[60px] border-l-transparent border-t-[60px] border-t-primary-500/10 opacity-0 group-hover:opacity-100 transition-all duration-500 transform rotate-45 translate-x-8 -translate-y-8"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  image: string;
  category: string;
  title: string;
  excerpt: string;
  authorName: string;
  authorRole: string;
  date: string;
  readTime: number;
}

const props = defineProps<Props>();

const authorInitial = computed(() => {
  return props.authorName.charAt(0).toUpperCase();
});

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', { 
    day: 'numeric', 
    month: 'short' 
  });
};
</script>

<style scoped>
/* Smooth transitions */
.group:hover .group-hover\:-translate-y-3 {
  transform: translateY(-0.75rem);
}

.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}

.group:hover .group-hover\:rotate-12 {
  transform: rotate(12deg);
}

/* Enhanced shadow on hover */
.group:hover .hover\:shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
