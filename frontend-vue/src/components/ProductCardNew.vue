<template>
  <router-link 
    :to="`/product/${product.id}`"
    class="group block"
  >
    <div class="relative bg-slate-800 dark:bg-slate-900 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 overflow-hidden border border-slate-700 dark:border-slate-600">
      <!-- Верхняя секция - основная информация -->
      <div class=" ">
        <!-- Верхние теги -->
        <div class="flex items-right justify-between mb-4 fixed p-3 w-full">
          <div >
            
          </div>
          <!-- Цена -->
          <div class="bg-purple-600 text-white px-3 py-1.5 rounded-full text-lg font-bold">
            {{ product.price }} ₽
          </div>
        </div>
        
        
        
        <!-- Изображение товара (на весь блок) -->
        <div class="w-full h-full  overflow-hidden bg-slate-700 dark:bg-slate-600">
          <img 
            v-if="hasImage"
            :src="imageSource" 
            :alt="product.title"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full bg-slate-600 dark:bg-slate-700 flex items-center justify-center">
            <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
      
      <!-- Нижняя секция - детали и кнопка -->
      <div class="bg-slate-700 dark:bg-slate-800 p-6 pt-4">
        <!-- Название товара (меньший размер) -->
        <h4 class="text-lg font-semibold text-white mb-3">
          {{ product.title }}
        </h4>
        
        <!-- Описание -->
        <p class="text-gray-300 text-sm mb-4 line-clamp-2">
          {{ product.description }}
        </p>
        
        <!-- Нижняя информация -->
        <div class="flex items-center justify-between">
          <!-- Количество -->
          <div class="text-white">
            <span class="text-sm">Количество: </span>
            <span class="text-purple-400 font-semibold">{{ product.quantity || 0 }}</span>
          </div>
          
          <!-- Кнопка покупки -->
          <button class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-6 py-2 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105">
            Купить
          </button>
        </div>
      </div>
      
      <!-- Hover эффект -->
      <div class="absolute inset-0 bg-gradient-to-t from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue';

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
  quantity?: number;
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
</style>
