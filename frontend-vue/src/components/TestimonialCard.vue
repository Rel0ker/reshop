<template>
  <div class="group relative bg-white dark:bg-slate-800 rounded-3xl p-6 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-500 border border-gray-100 dark:border-slate-700 overflow-hidden">
    <!-- Quote Icon -->
    <div class="absolute top-4 right-4 text-primary-200 dark:text-primary-800 opacity-20 group-hover:opacity-40 transition-opacity duration-500">
      <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24">
        <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
      </svg>
    </div>
    
    <!-- Content -->
    <div class="relative z-10">
      <!-- Rating -->
      <div class="flex items-center mb-4">
        <div class="flex items-center space-x-1">
          <svg 
            v-for="star in 5" 
            :key="star"
            class="w-5 h-5"
            :class="star <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300 dark:text-gray-600'"
            viewBox="0 0 20 20"
          >
            <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
          </svg>
        </div>
        <span class="ml-2 text-sm text-gray-500 dark:text-gray-400">{{ rating }}/5</span>
      </div>
      
      <!-- Review Text -->
      <blockquote class="text-gray-700 dark:text-gray-300 mb-6 leading-relaxed italic">
        "{{ review }}"
      </blockquote>
      
      <!-- User Info -->
      <div class="flex items-center">
        <div class="relative">
          <div class="w-12 h-12 bg-gradient-to-br from-primary-500 via-secondary-500 to-tertiary-500 rounded-full flex items-center justify-center mr-4 shadow-lg">
            <span class="text-white font-bold text-lg">
              {{ userInitial }}
            </span>
          </div>
          <div class="absolute -inset-1 bg-gradient-to-br from-primary-400 via-secondary-400 to-tertiary-400 rounded-full blur opacity-0 group-hover:opacity-75 transition-opacity duration-500"></div>
        </div>
        <div>
          <p class="font-semibold text-gray-900 dark:text-white">{{ userName }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ userRole }}</p>
        </div>
      </div>
    </div>
    
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5 group-hover:opacity-10 transition-opacity duration-500">
      <div class="absolute top-0 left-0 w-24 h-24 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full blur-2xl"></div>
      <div class="absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-br from-tertiary-400 to-primary-400 rounded-full blur-3xl"></div>
    </div>
    
    <!-- Hover Effect Border -->
    <div class="absolute inset-0 border-2 border-transparent group-hover:border-primary-500/20 rounded-3xl transition-all duration-500 pointer-events-none opacity-0 group-hover:opacity-100"></div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  rating: number;
  review: string;
  userName: string;
  userRole: string;
}

const props = defineProps<Props>();

const userInitial = computed(() => {
  return props.userName.charAt(0).toUpperCase();
});
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
