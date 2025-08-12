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
        <div v-for="product in products" :key="product.id" class="group bg-gray-900 border border-gray-700 rounded-2xl shadow-lg overflow-hidden flex flex-col transform hover:scale-105 transition-transform duration-300">
          <img :src="product.images.length > 0 ? product.images[0].image : noImage" alt="Product Image" class="w-full aspect-square object-cover"/>
          <div class="p-4 flex flex-col flex-grow">
            <h3 class="text-lg font-semibold text-white mb-2 flex-grow min-h-[56px]">{{ product.title }}</h3>
            <p class="text-2xl font-bold text-green-400 mb-4">{{ product.price }} ₽</p>
            <div class="flex items-center text-gray-400 text-sm mt-auto pt-2 border-t border-gray-600">
              <span>Продавец:</span>
              <span class="ml-2 font-medium text-gray-300 truncate">{{ product.seller.email }}</span>
            </div>
          </div>
        </div>
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

<style>
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