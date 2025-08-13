<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
    <!-- Animated Background -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
      <div class="absolute top-40 left-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 min-h-screen flex items-center justify-center p-4">
      <div class="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl shadow-2xl max-w-4xl w-full p-8">
        
        <!-- Success Header -->
        <div class="text-center mb-8">
          <div class="relative inline-block">
            <div class="w-24 h-24 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
              <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <div class="absolute -top-2 -right-2 w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center animate-bounce">
              <span class="text-xs font-bold text-gray-800">✓</span>
            </div>
          </div>
          
          <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent mb-4">
            Оплата прошла успешно!
          </h1>
          <p class="text-xl text-gray-300 max-w-2xl mx-auto">
            Спасибо за ваш заказ! Мы отправили подтверждение на ваш email. 
            Ваш цифровой товар будет доступен для скачивания в личном кабинете.
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-12">
          <div class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-white transition ease-in-out duration-150">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Загружаем детали заказа...
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <div class="bg-red-500/20 border border-red-500/50 rounded-2xl p-6">
            <svg class="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <h3 class="text-xl font-semibold text-red-400 mb-2">Ошибка загрузки</h3>
            <p class="text-red-300">{{ error }}</p>
          </div>
        </div>

        <!-- Order Details -->
        <div v-else-if="orderDetails" class="space-y-6">
          
          <!-- Order Summary Card -->
          <div class="bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-white/20 rounded-2xl p-6">
            <h2 class="text-2xl font-bold text-white mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              Детали заказа
            </h2>
            
            <div class="grid md:grid-cols-2 gap-6">
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-300">Номер заказа:</span>
                  <span class="font-mono font-semibold text-white bg-gray-800 px-3 py-1 rounded-lg">
                    {{ orderDetails.id.slice(0, 8) }}...
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-300">Дата заказа:</span>
                  <span class="text-white">{{ formatDate(new Date()) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-300">Статус:</span>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    <svg class="w-2 h-2 mr-1.5 text-green-400" fill="currentColor" viewBox="0 0 8 8">
                      <circle cx="4" cy="4" r="3" />
                    </svg>
                    Оплачен
                  </span>
                </div>
              </div>
              
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-300">Общая стоимость:</span>
                  <span class="text-2xl font-bold text-green-400">
                    {{ formatPrice(orderDetails.total_amount) }} ₽
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-300">Способ оплаты:</span>
                  <span class="text-white">Банковская карта</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Product Details -->
          <div class="bg-white/5 border border-white/10 rounded-2xl p-6">
            <h3 class="text-xl font-bold text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
              </svg>
              Купленные товары
            </h3>
            
            <div class="space-y-4">
              <div v-for="item in orderDetails.items" :key="item.product_name" 
                   class="bg-gradient-to-r from-gray-800/50 to-gray-700/50 border border-white/10 rounded-xl p-4 hover:border-purple-500/50 transition-all duration-300">
                
                <div class="flex items-start space-x-4">
                  <!-- Product Image -->
                  <div class="flex-shrink-0">
                    <img v-if="item.image_url" :src="item.image_url" :alt="item.product_name" 
                         class="w-20 h-20 object-cover rounded-lg border-2 border-white/20" />
                    <img v-else :src="noImage" :alt="item.product_name" 
                         class="w-20 h-20 object-cover rounded-lg border-2 border-white/20" />
                  </div>
                  
                  <!-- Product Info -->
                  <div class="flex-1 min-w-0">
                    <h4 class="text-lg font-semibold text-white mb-2">
                      {{ item.product_name }}
                    </h4>
                    
                    <div class="grid md:grid-cols-2 gap-4 text-sm">
                      <div class="space-y-2">
                        <div class="flex justify-between">
                          <span class="text-gray-400">Количество:</span>
                          <span class="text-white font-semibold">{{ item.quantity }} шт.</span>
                        </div>
                        <div class="flex justify-between">
                          <span class="text-gray-400">Цена за единицу:</span>
                          <span class="text-white">{{ formatPrice(item.price) }} ₽</span>
                        </div>
                        <div class="flex justify-between">
                          <span class="text-gray-400">Общая стоимость:</span>
                          <span class="text-green-400 font-semibold">{{ formatPrice(item.price * item.quantity) }} ₽</span>
                        </div>
                      </div>
                      
                      <div class="space-y-2">
                        <div v-if="item.seller_info" class="flex justify-between">
                          <span class="text-gray-400">Продавец:</span>
                          <span class="text-white">{{ item.seller_info }}</span>
                        </div>
                        <div v-if="item.usage_instructions" class="text-gray-300">
                          <span class="text-gray-400 block mb-1">Инструкция:</span>
                          <span class="text-sm">{{ truncateText(item.usage_instructions, 80) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Next Steps -->
          <div class="bg-gradient-to-r from-green-500/20 to-blue-500/20 border border-green-500/30 rounded-2xl p-6">
            <h3 class="text-xl font-bold text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Что дальше?
            </h3>
            
            <div class="grid md:grid-cols-3 gap-4 text-sm">
              <div class="text-center">
                <div class="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                  <span class="text-green-400 font-bold">1</span>
                </div>
                <p class="text-gray-300">Проверьте email с подтверждением</p>
              </div>
              <div class="text-center">
                <div class="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                  <span class="text-blue-400 font-bold">2</span>
                </div>
                <p class="text-gray-300">Скачайте товар в личном кабинете</p>
              </div>
              <div class="text-center">
                <div class="w-12 h-12 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                  <span class="text-purple-400 font-bold">3</span>
                </div>
                <p class="text-gray-300">Наслаждайтесь покупкой!</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center mt-8">
          <router-link
            to="/buyer"
            class="inline-flex items-center justify-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            В личный кабинет
          </router-link>
          
          <router-link
            to="/"
            class="inline-flex items-center justify-center px-8 py-4 bg-white/10 hover:bg-white/20 text-white font-bold rounded-2xl transition-all duration-300 border border-white/20 hover:border-white/40"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>
            На главную
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { api } from '../api';
import noImage from '../assets/no-image.png';

interface OrderItem {
  product_name: string;
  quantity: number;
  price: number;
  seller_info?: string;
  image_url?: string;
  usage_instructions?: string;
  description?: string;
}

interface OrderDetails {
  id: string;
  total_amount: string;
  items: OrderItem[];
  created_at?: string;
}

const route = useRoute();
const orderDetails = ref<OrderDetails | null>(null);
const isLoading = ref(true);
const error = ref<string | null>(null);

const props = defineProps({
  id: { type: String, required: true }
});

const truncateText = (text: string | undefined, maxLength: number): string => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

const formatPrice = (price: number | string): string => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  return numPrice.toLocaleString('ru-RU');
};

const formatDate = (date: Date): string => {
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

onMounted(async () => {
  const orderId = props.id;
  console.log('Order ID from URL:', orderId);

  if (!orderId) {
    error.value = 'Order ID not found in URL.';
    isLoading.value = false;
    return;
  }

  try {
    const response = await api.get(`/orders/${orderId}/`);
    console.log('Order details API response:', response.data);
    orderDetails.value = response.data;
  } catch (err) {
    console.error('Error fetching order details:', err);
    error.value = 'Failed to load order details.';
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>