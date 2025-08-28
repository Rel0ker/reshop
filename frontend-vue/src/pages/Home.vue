<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <!-- Hero Section -->
    <section class="relative overflow-hidden">
      <div class="relative z-10 container mx-auto px-4 pt-20 pb-16">
        <div class="text-center max-w-4xl mx-auto">
          <div class="inline-flex items-center px-4 py-2 bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200 rounded-full text-sm font-medium mb-8 animate-fade-in">
            <span class="w-2 h-2 bg-purple-500 rounded-full mr-2 animate-pulse"></span>
            Re:shop в закрытом бета-тесте
          </div>
          
          <h1 class="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight animate-fade-in animation-delay-200">
            Новый. Быстрый.
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600">
              Безопасный.
            </span>
          </h1>
          
          <p class="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto animate-fade-in animation-delay-400">
            Откройте для себя мир качественных цифровых товаров от проверенных продавцов
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center animate-fade-in animation-delay-600">
            <router-link
              to="/popular"
              class="group relative px-8 py-4 bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 text-white font-semibold rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 overflow-hidden"
            >
              <span class="relative z-10">Перейти в каталог</span>
              <div class="absolute inset-0 bg-gradient-to-r from-purple-700 via-pink-700 to-rose-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link>
            
            <router-link
              to="/register"
              class="px-8 py-4 border-2 border-purple-600 text-purple-600 dark:text-purple-400 font-semibold rounded-2xl hover:bg-purple-600 hover:text-white transition-all duration-300 hover:scale-105"
            >
              Стать продавцом
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-white dark:bg-slate-800/50">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-8">
          Добро пожаловать в Re:shop!
        </h2>
        <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-8">
          Ваш надежный маркетплейс цифровых товаров
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-6 bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 rounded-2xl">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Быстрая доставка</h3>
            <p class="text-gray-600 dark:text-gray-300">Получите товар мгновенно</p>
          </div>
          <div class="p-6 bg-gradient-to-br from-blue-100 to-cyan-100 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-2xl">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Гарантия качества</h3>
            <p class="text-gray-600 dark:text-gray-300">Все товары проверены</p>
          </div>
          <div class="p-6 bg-gradient-to-br from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-cyan-900/30 rounded-2xl">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Безопасные платежи</h3>
            <p class="text-gray-600 dark:text-gray-300">Защищенные транзакции</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Popular Products Section with Smooth Transition -->
    <section class="py-20 bg-gradient-to-br from-slate-100 via-purple-50 to-pink-50 dark:from-slate-800 dark:via-purple-900/20 dark:to-pink-900/20">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-5xl font-extrabold text-gray-900 dark:text-white mb-6">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600">
              Популярные товары
            </span>
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Откройте для себя лучшие цифровые товары от проверенных продавцов
          </p>
        </div>

        <!-- Products Grid -->
        <div v-if="products.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          <ProductCardNew 
            v-for="product in products" 
            :key="product.id" 
            :product="product" 
          />
        </div>

        <!-- Loading State -->
        <div v-else class="text-center py-16">
          <div class="max-w-md mx-auto">
            <!-- Animated Loading Icon -->
            <div class="relative mb-6">
              <div class="w-20 h-20 mx-auto relative">
                <!-- Outer ring -->
                <div class="absolute inset-0 border-4 border-purple-200 dark:border-purple-800 rounded-full"></div>
                <!-- Animated ring -->
                <div class="absolute inset-0 border-4 border-transparent border-t-purple-600 dark:border-t-purple-400 rounded-full animate-spin"></div>
                <!-- Center icon -->
                <div class="absolute inset-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                  <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
              </div>
            </div>
            
            <!-- Loading Text -->
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Ищем лучшие товары для вас
            </h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Это займет всего несколько секунд...
            </p>
            
            <!-- Progress Bar -->
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
              <div class="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full animate-pulse" style="width: 60%"></div>
            </div>
            
            <!-- Loading Dots -->
            <div class="flex justify-center space-x-2">
              <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>

        <!-- Load More Button -->
        <div v-if="nextPageUrl" class="text-center mt-16">
          <button 
            @click="loadMore" 
            class="group relative px-8 py-4 bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 text-white font-semibold rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 overflow-hidden"
          >
            <span class="relative z-10">Загрузить еще</span>
            <div class="absolute inset-0 bg-gradient-to-r from-purple-700 via-pink-700 to-rose-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
        </div>

        <!-- CTA Section -->
        <div class="text-center mt-20">
          <div class="bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 rounded-3xl p-12 text-white">
            <h3 class="text-3xl font-bold mb-4">Готовы начать?</h3>
            <p class="text-xl mb-8 opacity-90">Присоединяйтесь к тысячам довольных покупателей</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link
                to="/register"
                class="px-8 py-4 bg-white text-purple-600 font-semibold rounded-2xl hover:bg-gray-100 transition-all duration-300 hover:scale-105"
              >
                Создать аккаунт
              </router-link>
              <router-link
                to="/popular"
                class="px-8 py-4 border-2 border-white text-white font-semibold rounded-2xl hover:bg-white hover:text-purple-600 transition-all duration-300 hover:scale-105"
              >
                Смотреть все товары
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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
    console.log('Запрашиваю товары по URL:', url);
    const response = await api.get<{ results: Product[], next: string | null }>(url);
    console.log('Ответ от API:', response.data);
    products.value.push(...response.data.results);
    nextPageUrl.value = response.data.next;
    console.log('Товары загружены:', products.value);
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

<style scoped>
.animation-delay-200 {
  animation-delay: 200ms;
}

.animation-delay-400 {
  animation-delay: 400ms;
}

.animation-delay-600 {
  animation-delay: 600ms;
}

.animate-fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Smooth scroll behavior */
html {
  scroll-behavior: smooth;
}
</style>