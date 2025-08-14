<template>
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
    
    <!-- Нижняя секция - детали и кнопки -->
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
      <div class="flex items-center justify-between mb-4">
        <!-- Количество -->
        <div class="text-white">
          <span class="text-sm">Количество: </span>
          <span class="text-purple-400 font-semibold">{{ product.quantity || 0 }}</span>
        </div>
        
        <!-- Дата создания -->
        <div class="text-gray-400 text-xs">
          {{ formatDate(product.created_at) }}
        </div>
      </div>
      
      <!-- Кнопки действий -->
      <div class="flex gap-3">
        <!-- Кнопка редактирования -->
        <button 
          @click="$emit('edit', product)"
          class="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Редактировать
        </button>
        
        <!-- Кнопка удаления -->
        <button 
          @click="$emit('delete', product.id)"
          class="flex-1 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Удалить
        </button>
      </div>
    </div>
    
    <!-- Hover эффект -->
    <div class="absolute inset-0 bg-gradient-to-t from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
  </div>
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
  created_at: string;
}

const props = defineProps<{
  product: Product;
}>();

const emit = defineEmits<{
  edit: [product: Product];
  delete: [productId: string];
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

// Форматирование даты
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
