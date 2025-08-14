<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <div class="container mx-auto px-4 py-8">
      <!-- Search Header -->
      <div class="text-center mb-8 animate-fade-in">
        <div class="relative">
          <div class="absolute inset-0 bg-gradient-to-r from-purple-400/20 via-pink-400/20 to-rose-400/20 dark:from-purple-600/20 dark:via-pink-600/20 dark:to-rose-600/20 rounded-full blur-3xl"></div>
          <h1 class="relative text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 animate-gradient">
              Результаты поиска
            </span>
          </h1>
        </div>
        <p class="text-xl text-gray-600 dark:text-gray-300 mb-2">
          Поиск по запросу: <span class="font-semibold text-purple-600 dark:text-pink-500">"{{ searchQuery }}"</span>
        </p>
        <p class="text-gray-500 dark:text-gray-400">
          Найдено товаров: <span class="font-semibold text-purple-600 dark:text-pink-500">{{ totalResults }}</span>
        </p>
      </div>

      <!-- Search Results -->
      <div v-if="!loading" class="animate-fade-in stagger-1">
        <!-- Empty State -->
        <div v-if="products.length === 0" class="text-center py-16">
          <div class="max-w-md mx-auto">
            <div class="text-6xl mb-4">🔍</div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Товары не найдены</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Попробуйте изменить параметры поиска или вернуться к каталогу
            </p>
            <div class="flex gap-4 justify-center">
              <button
                @click="clearSearch"
                class="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-xl font-medium transition-colors duration-300"
              >
                Очистить поиск
              </button>
              <router-link
                to="/popular"
                class="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-medium transition-colors duration-300"
              >
                Перейти в каталог
              </router-link>
            </div>
          </div>
        </div>

        <!-- Products Grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <ProductCardNew
            v-for="(product, index) in products"
            :key="product.id"
            :product="product"
            @click="goToProduct(product.id)"
            :style="{ animationDelay: `${index * 0.1}s` }"
          />
        </div>

        <!-- Load More Button -->
        <div v-if="hasMore" class="text-center mt-12">
          <button
            @click="loadMore"
            :disabled="loadingMore"
            class="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-400 disabled:to-gray-500 text-white rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 disabled:transform-none disabled:cursor-not-allowed"
          >
            <div v-if="loadingMore" class="flex items-center gap-2">
              <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Загрузка...
            </div>
            <div v-else class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
              Загрузить еще
            </div>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-else class="text-center py-16">
        <div class="max-w-md mx-auto">
          <div class="relative mb-8">
            <div class="w-24 h-24 border-4 border-purple-200 dark:border-purple-800 rounded-full mx-auto"></div>
            <div class="absolute inset-0 w-24 h-24 border-4 border-purple-600 border-t-transparent rounded-full mx-auto animate-spin"></div>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Поиск товаров</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">Пожалуйста, подождите...</p>
          <div class="flex justify-center gap-2">
            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
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
</style>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from '../api';
import OrderModal from '../components/OrderModal.vue';
import ProductCardNew from '@/components/ProductCardNew.vue';

const route = useRoute();
const router = useRouter();

// Search state
const searchQuery = computed(() => route.query.q as string || '');
const products = ref<any[]>([]);
const loading = ref(false);
const loadingMore = ref(false);
const totalResults = ref(0);
const hasMore = ref(true);
const page = ref(1);

// Modal state
const isOrderModalVisible = ref(false);
const selectedProduct = ref<any>(null);

// Fetch search results
const fetchSearchResults = async (isLoadMore = false) => {
  if (!searchQuery.value) return;

  try {
    if (isLoadMore) {
      loadingMore.value = true;
    } else {
      loading.value = true;
      page.value = 1;
      products.value = [];
    }

    // Экранируем специальные символы для поиска
    const escapedQuery = searchQuery.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    const response = await api.get(`/products/`, {
      params: {
        search: escapedQuery,
        page: page.value,
        limit: 20
      }
    });

    console.log('🔍 Search results:', response.data);

    const newProducts = response.data.results || [];
    
    if (isLoadMore) {
      products.value.push(...newProducts);
    } else {
      products.value = newProducts;
    }

    totalResults.value = response.data.count || 0;
    hasMore.value = response.data.next !== null;
    
    if (hasMore.value) {
      page.value++;
    }
  } catch (error) {
    console.error('Ошибка поиска:', error);
  } finally {
    loading.value = false;
    loadingMore.value = false;
  }
};

// Load more products
const loadMore = () => {
  if (!loadingMore.value && hasMore.value) {
    fetchSearchResults(true);
  }
};

// Clear search and go back
const clearSearch = () => {
  router.push('/popular');
};

// Navigation
const goToProduct = (productId: string) => {
  router.push(`/product/${productId}`);
};

// Order modal
const openOrderModal = (product: any) => {
  selectedProduct.value = product;
  isOrderModalVisible.value = true;
};

const closeOrderModal = () => {
  isOrderModalVisible.value = false;
  selectedProduct.value = null;
};

const handleOrderSuccess = () => {
  console.log('Order placed successfully from Search!');
  closeOrderModal();
};

// Watch for route changes
onMounted(() => {
  if (searchQuery.value) {
    fetchSearchResults();
  }
});
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

.stagger-1 {
  animation-delay: 0.1s;
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

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 