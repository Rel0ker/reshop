<template>
  <router-link 
    :to="`/product/${product.id}`"
    class="group block"
  >
    <div class="relative bg-white dark:bg-slate-800 rounded-3xl shadow-lg hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 overflow-hidden border border-gray-100 dark:border-slate-700">
      <!-- Image Container -->
      <div class="relative overflow-hidden">
        <img 
          v-if="hasImage"
          :src="imageSource" 
          :alt="product.title"
          class="w-full aspect-square object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
        />
        <ProductImagePlaceholder 
          v-else
          class="w-full aspect-square"
          text="Фото товара"
          subtitle="Изображение не загружено"
        />
        
        <!-- Overlay with gradient -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/30 via-black/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        
        <!-- Price Badge -->
        <div class="absolute top-3 right-3 bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg border border-gray-200/50 dark:border-slate-600/50 transform group-hover:scale-110 transition-all duration-300">
          <span class="text-lg font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            {{ product.price }} ₽
          </span>
        </div>
        
        <!-- Rating Badge -->
        <div class="absolute top-3 left-3 bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm px-3 py-2 rounded-full shadow-lg border border-gray-200/50 dark:border-slate-600/50 transform group-hover:scale-110 transition-all duration-300">
          <div class="flex items-center text-yellow-500">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
              <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
            </svg>
            <span class="ml-1 text-sm font-medium text-gray-700 dark:text-gray-300">4.8</span>
          </div>
        </div>

        <!-- New Badge -->
        <div class="absolute bottom-3 left-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-3 py-1.5 rounded-full text-xs font-semibold shadow-lg transform group-hover:scale-110 transition-all duration-300">
          Новинка
        </div>

        <!-- Hover Action Button -->
        <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex items-center justify-center">
          <div class="bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm px-6 py-3 rounded-2xl shadow-xl transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
            <span class="text-gray-900 dark:text-white font-semibold">Смотреть детали</span>
          </div>
        </div>
      </div>
      
      <!-- Content -->
      <div class="p-6">
        <!-- Title -->
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3 line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300">
          {{ product.title }}
        </h3>
        
        <!-- Description Preview -->
        <p class="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2">
          {{ product.description }}
        </p>
        
        <!-- Tags -->
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs rounded-full">
            Цифровой товар
          </span>
          <span class="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/30 text-secondary-700 dark:text-secondary-300 text-xs rounded-full">
            Мгновенная доставка
          </span>
        </div>
        
        <!-- Seller Info -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="relative">
              <div class="w-10 h-10 bg-gradient-to-br from-primary-500 via-secondary-500 to-tertiary-500 rounded-full flex items-center justify-center mr-3 shadow-lg">
                <span class="text-white text-sm font-bold">
                  {{ (product.seller && product.seller.email) ? product.seller.email.charAt(0).toUpperCase() : 'U' }}
                </span>
              </div>
              <div class="absolute -inset-1 bg-gradient-to-br from-primary-400 via-secondary-400 to-tertiary-400 rounded-full blur opacity-0 group-hover:opacity-75 transition-opacity duration-500"></div>
            </div>
            <div class="text-sm">
              <p class="text-gray-700 dark:text-gray-300 font-medium">Продавец</p>
              <p class="text-gray-500 dark:text-gray-400 truncate max-w-[120px]">
                {{ (product.seller && product.seller.email) ? product.seller.email : 'Неизвестный продавец' }}
              </p>
            </div>
          </div>
          
          <!-- Action Icon -->
          <div class="w-10 h-10 bg-gray-100 dark:bg-slate-700 rounded-full flex items-center justify-center group-hover:bg-gradient-to-r group-hover:from-primary-500 group-hover:to-secondary-500 transition-all duration-300 transform group-hover:scale-110 group-hover:rotate-12">
            <svg class="w-5 h-5 text-gray-500 group-hover:text-white transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
      
      <!-- Hover Effect Border -->
      <div class="absolute inset-0 border-2 border-transparent group-hover:border-primary-500 rounded-3xl transition-all duration-500 pointer-events-none opacity-0 group-hover:opacity-100"></div>
      
      <!-- Corner Accent -->
      <div class="absolute top-0 right-0 w-0 h-0 border-l-[50px] border-t-[50px] border-l-transparent border-t-primary-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import ProductImagePlaceholder from './ProductImagePlaceholder.vue';

interface Seller {
  id: string;
  email: string;
}

interface ProductImage {
  id: string;
  image: string;
  product: string;
}

interface Product {
  id: string;
  title: string;
  description: string;
  price: string;
  seller: Seller;
  images: ProductImage[];
  image_url?: string;
}

const props = defineProps<{
  product: Product;
}>();

// Computed properties for image handling
const hasImage = computed(() => {
  return (props.product.images && props.product.images.length > 0) || props.product.image_url;
});

const imageSource = computed(() => {
  if (props.product.images && props.product.images.length > 0) {
    return props.product.images[0].image;
  }
  return props.product.image_url || '';
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Smooth hover transitions */
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}

.group:hover .group-hover\:-translate-y-3 {
  transform: translateY(-0.75rem);
}

/* Enhanced shadow on hover */
.group:hover .hover\:shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Smooth image scale */
.group:hover img {
  transform: scale(1.1);
}

/* Corner accent animation */
.group:hover .corner-accent {
  transform: rotate(45deg) scale(1.1);
}
</style>