<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api';
import OrderModal from '../components/OrderModal.vue';
import SortDropdown from '../components/SortDropdown.vue';
import noImage from '../assets/no-image.png';

interface Product {
  id: string;
  title: string;
  description: string;
  price: string;
  quantity: number;
  download_link: string;
  image_url?: string;
  seller_info?: string;
  seller_rating?: number;
  images?: { id: string; image: string }[]; // Added for multiple images
}

const products = ref<Product[]>([]);
const page = ref(1);
const pageSize = 24;
const loading = ref(false);
const hasMore = ref(true);
const isOrderModalVisible = ref(false);
const selectedProduct = ref<Product | null>(null);
const searchQuery = ref('');
const sortBy = ref('popular');

const router = useRouter();

const sortOptions = [
  { id: 'popular', name: 'По популярности', icon: '🔥' },
  { id: 'price_low', name: 'По цене (сначала дешевые)', icon: '💰' },
  { id: 'price_high', name: 'По цене (сначала дорогие)', icon: '💎' },
  { id: 'newest', name: 'По дате', icon: '🆕' }
];

// Короткие названия для мобильной версии
const sortOptionsShort = [
  { id: 'popular', name: 'Популярные', icon: '🔥' },
  { id: 'price_low', name: 'Дешевые', icon: '💰' },
  { id: 'price_high', name: 'Дорогие', icon: '💎' },
  { id: 'newest', name: 'Новые', icon: '🆕' }
];

const fetchProducts = async () => {
  if (loading.value || !hasMore.value) return;
  loading.value = true;
  try {
    const response = await api.get(`/products/?page=${page.value}&page_size=${pageSize}`);
    const newProducts: Product[] = response.data.results;
    if (newProducts.length > 0) {
      products.value.push(...newProducts);
      page.value++;
    } else {
      hasMore.value = false;
    }
  } catch (error) {
    console.error("Ошибка при загрузке товаров:", error);
    hasMore.value = false;
  } finally {
    loading.value = false;
  }
};

// Функция для обновления товара в списке
const updateProductInList = (updatedProduct: Product) => {
  const index = products.value.findIndex(p => p.id === updatedProduct.id);
  if (index !== -1) {
    products.value[index] = updatedProduct;
    console.log('🔄 Product updated in catalog list:', updatedProduct.id);
  }
};

// Функция для обновления списка товаров
const refreshProducts = async () => {
  console.log('🔄 Refreshing products list...');
  products.value = [];
  page.value = 1;
  hasMore.value = true;
  await fetchProducts();
};

const handleScroll = () => {
  const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight >= document.documentElement.offsetHeight - 100;
  if (bottomOfWindow && hasMore.value && !loading.value) {
    fetchProducts();
  }
};

onMounted(() => {
  fetchProducts();
  window.addEventListener('scroll', handleScroll);
  
  // Добавляем обработчик для обновления при фокусе на странице
  window.addEventListener('focus', () => {
    console.log('🔄 Page focused, checking if products need refresh...');
    // Можно добавить логику для проверки, нужно ли обновлять товары
  });
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('focus', () => {});
});

const openOrderModal = (product: Product) => {
  selectedProduct.value = product;
  isOrderModalVisible.value = true;
};

const closeOrderModal = () => {
  isOrderModalVisible.value = false;
  selectedProduct.value = null;
};

const handleOrderSuccess = () => {
  console.log('Order placed successfully from PopularProducts!');
};

const goToProduct = (productId: string) => {
  router.push(`/product/${productId}`);
};

const filteredProducts = computed(() => {
  let filtered = products.value;
  
  if (searchQuery.value) {
    filtered = filtered.filter(product => 
      product.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      product.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }
  
  return filtered;
});

const sortedProducts = computed(() => {
  const products = [...filteredProducts.value];
  
  switch (sortBy.value) {
    case 'price_low':
      return products.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
    case 'price_high':
      return products.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
    case 'newest':
      return products; // Уже отсортировано по дате создания
    default:
      return products; // По популярности (как есть)
  }
});
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <!-- Hero Section -->
    <div class="relative ">
      <div class="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-pink-600/20 dark:from-purple-600/10 dark:to-pink-600/10"></div>
      <div class="relative container mx-auto px-4 py-16">
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 bg-clip-text text-transparent">
            Цифровые товары
          </h1>
          <p class="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            Откройте для себя уникальные цифровые продукты от талантливых создателей
          </p>
          
          <!-- Search Bar -->
          <div class="max-w-4xl mx-auto mb-8">
            <div class="flex flex-col lg:flex-row gap-4 items-center justify-center">
              <!-- Search Input -->
              <div class="relative flex-1 max-w-2xl">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Поиск товаров..."
                  class="w-full px-6 py-4 bg-white/80 dark:bg-white/10 backdrop-blur-md border border-gray-200 dark:border-white/20 rounded-2xl text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                />
                <div class="absolute right-4 top-1/2 transform -translate-y-1/2">
                  <svg class="w-6 h-6 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
              
              <!-- Sort Dropdown -->
              <div class="relative flex items-center gap-4">
                <button
                  @click="refreshProducts"
                  class="flex items-center gap-3 px-6 py-4 bg-white/80 dark:bg-white/10 backdrop-blur-md border border-gray-200 dark:border-white/20 rounded-2xl cursor-pointer hover:bg-white/90 dark:hover:bg-white/20 transition-all duration-300 hover:border-purple-500/50 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                >
                  <svg class="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span class="text-gray-700 dark:text-gray-200 font-medium">Обновить</span>
                </button>
                
                <SortDropdown 
                  v-model="sortBy"
                  :options="sortOptions"
                  label="Сортировка"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

   

    <!-- Products Grid -->
    <div class="container mx-auto px-4 pb-16">
      <!-- Empty State -->
      <div v-if="sortedProducts.length === 0 && !loading" class="text-center py-16">
        <div class="max-w-md mx-auto">
          <div class="text-6xl mb-4">🔍</div>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Товары не найдены</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            Попробуйте изменить параметры поиска
          </p>
          <button
            @click="searchQuery = ''"
            class="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-medium transition-colors duration-300"
          >
            Сбросить фильтры
          </button>
        </div>
      </div>

      <!-- Products Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mt-10">
        <div
          v-for="(product, index) in sortedProducts"
          :key="product.id"
          @click="goToProduct(product.id)"
          class="group bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-2xl overflow-hidden hover:border-purple-500/50 transition-all duration-500 hover:shadow-2xl hover:shadow-2xl hover:shadow-purple-500/20 transform hover:-translate-y-2 cursor-pointer"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- Product Image -->
          <div class="relative aspect-square overflow-hidden">
            <img
              :src="product.images && product.images.length > 0 ? product.images[0].image : (product.image_url || noImage)"
              :alt="product.title"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <!-- Price Badge -->
            <div class="absolute top-4 right-4 bg-purple-600/90 backdrop-blur-sm px-3 py-2 rounded-full shadow-lg">
              <span class="text-white font-bold text-lg">{{ product.price }} ₽</span>
            </div>

            <!-- Status Badge -->
            <div class="absolute top-4 left-4">
              <span
                :class="[
                  'px-3 py-1 rounded-full text-xs font-semibold',
                  product.quantity > 0
                    ? 'bg-green-500/90 text-white'
                    : 'bg-red-500/90 text-white'
                ]"
              >
                {{ product.quantity > 0 ? 'В наличии' : 'Нет в наличии' }}
              </span>
            </div>
          </div>

          <!-- Product Content -->
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3 line-clamp-2 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors duration-300 flex items-center gap-2">
              {{ product.title }}
              <span class="text-xs text-gray-500 dark:text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300">👆</span>
            </h3>
            
            <p class="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-3 leading-relaxed">
              {{ product.description }}
            </p>

            <!-- Seller Info -->
            <div v-if="product.seller_info" class="mb-4 p-3 bg-gray-50 dark:bg-white/5 rounded-xl border border-gray-200 dark:border-white/10">
              <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">От продавца:</p>
              <p class="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">{{ product.seller_info }}</p>
            </div>

            <!-- Seller Rating -->
            <div v-if="product.seller_rating" class="mb-4 flex items-center gap-2">
              <div class="flex items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400 mr-2">Оценка продавца:</span>
                <div class="flex items-center">
                  <span class="text-yellow-500 text-lg mr-1">⭐</span>
                  <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ product.seller_rating }}/5</span>
                </div>
              </div>
            </div>

            <!-- Action Button -->
            <div class="flex justify-between items-center">
              <div class="text-sm text-gray-600 dark:text-gray-400">
                Количество: <span class="text-purple-600 dark:text-purple-400 font-semibold">{{ product.quantity }}</span>
              </div>
              
              <button
                @click.stop="openOrderModal(product)"
                :disabled="product.quantity === 0"
                :class="[
                  'px-6 py-3 rounded-xl font-semibold transition-all duration-300 transform group-hover:scale-105',
                  product.quantity > 0
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-600/25'
                    : 'bg-gray-600 text-gray-400 cursor-not-allowed'
                ]"
              >
                {{ product.quantity === 0 ? 'Нет в наличии' : 'Купить' }}
              </button>
            </div>
          </div>

          <!-- Hover Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-purple-600/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-flex items-center gap-3">
          <div class="w-6 h-6 border-2 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-gray-600 dark:text-gray-400 text-lg">Загрузка товаров...</span>
        </div>
      </div>

      <!-- End of Results -->
      <div v-if="!hasMore && sortedProducts.length > 0" class="text-center py-16">
        <div class="max-w-md mx-auto">
          <div class="text-4xl mb-4">✨</div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Все товары загружены</h3>
          <p class="text-gray-600 dark:text-gray-400">Вы просмотрели все доступные товары</p>
        </div>
      </div>
    </div>

    <!-- Order Modal -->
    <OrderModal
      :isVisible="isOrderModalVisible"
      :product="selectedProduct"
      @close="closeOrderModal"
      @orderSuccess="handleOrderSuccess"
    />
  </div>
</template>

<style scoped>
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

/* Animation for products appearing */
.grid > div {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(30px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Animation for results count block */
.animate-fade-in-up {
  animation: fadeInUpResults 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeInUpResults {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>