<template>
  <div class="bg-black text-gray-200 min-h-screen relative">
    <div 
      class="absolute inset-0 z-0 bg-gradient-to-br from-black via-gray-900/40 to-black"
      style="background-image: radial-gradient(circle at top right, rgba(128, 0, 128, 0.1), transparent 50%), radial-gradient(circle at bottom left, rgba(0, 0, 255, 0.1), transparent 50%);"
    ></div>
    <div class="container mx-auto px-4 py-8 relative z-10">
      <h1 class="text-5xl font-extrabold text-white text-center mb-12">
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-500">
          Каталог товаров
        </span>
      </h1>

      <div v-if="products.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        <ProductCardNew 
          v-for="product in products" 
          :key="product.id" 
          :product="product"
        />
      </div>
      <div v-else class="text-center py-16 text-gray-500">
        <p>Загрузка товаров или здесь пока пусто...</p>
      </div>

      <div v-if="nextPageUrl" class="text-center mt-16">
        <button @click="loadMore" class="w-full max-w-sm bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-4 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50 transition-all duration-300 animate-pulse-slow hover:animate-none shadow-lg shadow-purple-500/20">
          Загрузить еще
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes pulse-slow {
  50% {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.4);
  }
}
.animate-pulse-slow {
  animation: pulse-slow 3s infinite;
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../api';
import noImage from '../assets/no-image.png';
import ProductCardNew from '@/components/ProductCardNew.vue';

interface Seller {
  id: string;
  email: string;
  role: string;
}

interface ProductImage {
  id: string;
  image: string;
}

interface Product {
  id: string;
  title: string;
  description: string;
  price: string;
  quantity?: number;
  seller: Seller;
  images: ProductImage[];
}

const products = ref<Product[]>([]);
const nextPageUrl = ref<string | null>(null);

const fetchProducts = async (url: string) => {
  try {
    const response = await api.get<{ results: Product[], next: string | null }>(url);
    products.value.push(...response.data.results);
    nextPageUrl.value = response.data.next;
  } catch (error) {
    console.error('Ошибка при загрузке товаров:', error);
  }
};

const loadMore = () => {
  if (nextPageUrl.value) {
    const urlObject = new URL(nextPageUrl.value);
    fetchProducts(urlObject.pathname + urlObject.search);
  }
};

onMounted(() => {
  fetchProducts('/products/');
});
</script> 