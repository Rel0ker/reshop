<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { marked } from 'marked';
import { api } from "../api";
import { useAuth } from "../store";
import ProductCard from "../components/ProductCard.vue";
import noImage from "../assets/no-image.png";

interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  quantity: number;
  download_link: string;
  seller_info?: string;
  image_url?: string;
  usage_instructions?: string;
  seller: {
    id: string;
  };
  images?: { image: string }[];
}

interface OrderItem {
  id: string;
  title: string;
  description: string;
  quantity: number;
  price: number;
  download_link: string;
  seller_info?: string;
  image_url?: string;
  usage_instructions?: string;
  seller: {
    id: string;
  };
}

interface Order {
  id: string;
  product: Product;
  status: string;
  created_at: string;
  total_amount: string;
  items: OrderItem[];
  comment?: string;
  quantity: number;
}

const showOrderDetailsModal = ref(false);
const selectedOrder = ref<Order | null>(null);

function openOrderDetailsModal(order: Order) {
  selectedOrder.value = order;
  showOrderDetailsModal.value = true;
}

function closeOrderDetailsModal() {
  showOrderDetailsModal.value = false;
  selectedOrder.value = null;
}

const auth = useAuth();
const orders = ref<Order[]>([]);

onMounted(async () => {
  await fetchOrders();
});

async function fetchOrders() {
  try {
    const { data } = await api.get("/orders/mine/");
    console.log('Orders data:', data);
    
    // Проверяем, что data является массивом
    if (Array.isArray(data)) {
      orders.value = data.map((order: Order) => ({
        ...order,
        product: {
          ...order.product,
          title: order.product.title || `Товар без названия`,
        },
      })).sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    } else {
      console.error('Orders data is not an array:', data);
      orders.value = [];
    }
  } catch (error) {
    console.error('Error fetching orders:', error);
    orders.value = [];
  }
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': 'В ожидании оплаты',
    'paid': 'Оплачен',
    'delivered': 'Завершен',
    'payment_rejected': 'Отклонен платежной системой',
    'seller_rejected': 'Отклонен продавцом',
    'canceled': 'Отменен'
  };
  return statusMap[status] || status;
};

const renderedUsageInstructions = (text: string) => {
  return marked(text || '');
};

const renderedDescription = (text: string) => {
  return marked(text || '');
};

const getStatusColor = (status: string) => {
  const colorMap: Record<string, string> = {
    'pending': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    'paid': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    'delivered': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    'payment_rejected': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    'seller_rejected': 'bg-red-500 text-white dark:bg-red-600',
    'canceled': 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400';
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-purple-600/20 via-blue-600/20 to-indigo-600/20"></div>
      <div class="relative container mx-auto px-4 py-16">
        <div class="text-center">
          <h1 class="text-5xl md:text-6xl font-bold bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            Личный кабинет
          </h1>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Управляйте своими заказами, отслеживайте статус доставки и получайте доступ к купленным товарам
          </p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 pb-16 mt-16">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Всего заказов</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ orders.length }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Активные заказы</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ orders.filter(o => o.status === 'pending' || o.status === 'paid').length }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Завершенные заказы</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ orders.filter(o => o.status === 'delivered').length }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Orders Section -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Мои заказы</h2>
          <div class="flex space-x-3">
            <button class="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-medium hover:from-purple-700 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 shadow-lg">
              Все заказы
            </button>
          </div>
        </div>

        <!-- Orders Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="(order, index) in orders" 
            :key="order.id" 
            class="group bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 cursor-pointer border border-gray-200/50 dark:border-slate-700/50 overflow-hidden"
            :style="{ animationDelay: `${index * 100}ms` }"
            @click="openOrderDetailsModal(order)"
          >
            <!-- Order Header -->
            <div class="p-6 border-b border-gray-100 dark:border-slate-700">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                  Заказ #{{ order.id.substring(0, 8) }}
                </h3>
                <span 
                  :class="[
                    'px-3 py-1.5 text-xs font-semibold rounded-full shadow-sm',
                    getStatusColor(order.status)
                  ]"
                >
                  {{ getStatusText(order.status) }}
                </span>
              </div>
              
              <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ new Date(order.created_at).toLocaleDateString('ru-RU', { 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                }) }}
              </div>
            </div>

            <!-- Product Info -->
            <div class="p-6">
              <div class="flex items-center space-x-4 mb-4">
                <div class="w-16 h-16 rounded-xl overflow-hidden bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-800 dark:to-blue-800 flex-shrink-0 shadow-sm">
                  <img 
                    :src="order.product.images && order.product.images.length > 0 ? order.product.images[0].image : (order.product.image_url || noImage)" 
                    :alt="order.product.title"
                    class="w-full h-full object-cover"
                    @error="(event) => { const target = event.target as HTMLImageElement; if (target) target.src = noImage; }"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="font-semibold text-gray-900 dark:text-white text-sm leading-tight mb-1 line-clamp-2">
                    {{ order.product.title }}
                  </h4>
                  <p class="text-xs text-gray-500 dark:text-gray-400 line-clamp-1">
                    {{ order.product.description }}
                  </p>
                </div>
              </div>

              <!-- Order Summary -->
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Количество:</span>
                  <span class="font-medium text-gray-900 dark:text-white">{{ order.quantity }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Цена за ед.:</span>
                  <span class="font-medium text-gray-900 dark:text-white">{{ order.product.price }} ₽</span>
                </div>
                <div class="pt-3 border-t border-gray-100 dark:border-slate-700">
                  <div class="flex justify-between items-center">
                    <span class="text-lg font-bold text-gray-900 dark:text-white">Итого:</span>
                    <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                      {{ order.total_amount }} ₽
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Button -->
            <div class="p-6 pt-0" v-if="order.status !== 'seller_rejected' && order.status !== 'payment_rejected' && order.status !== 'canceled'">
              <button class="w-full py-3 bg-gradient-to-r from-gray-100 to-gray-200 dark:from-slate-700 dark:to-slate-600 text-gray-700 dark:text-gray-300 rounded-xl font-medium hover:from-purple-100 hover:to-blue-100 dark:hover:from-purple-800 dark:hover:to-blue-800 hover:text-purple-700 dark:hover:text-purple-400 transition-all duration-300 transform hover:scale-105">
                Подробнее
              </button>
            </div>
            
            <!-- Статус для отклоненных заказов -->
            <div v-else class="p-6 pt-0">
              <div class="text-center py-3 px-4 rounded-lg font-medium text-sm"
                   :class="getStatusColor(order.status)">
                {{ getStatusText(order.status) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="orders.length === 0" class="text-center py-16">
          <div class="max-w-md mx-auto">
            <div class="w-24 h-24 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-800 dark:to-blue-800 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-12 h-12 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">У вас пока нет заказов</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">Отправляйтесь в каталог и найдите товары, которые вам нужны</p>
            <router-link to="/popular" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-medium hover:from-purple-700 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 shadow-lg">
              Перейти в каталог
              <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Order Details Modal -->
    <div v-if="showOrderDetailsModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto relative">
        <!-- Modal Header -->
        <div class="sticky top-0 bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700 p-6 rounded-t-2xl">
          <div class="flex items-center justify-between">
            <h2 class="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Заказ #{{ selectedOrder?.id.substring(0, 8) }}
            </h2>
            <button 
              @click="closeOrderDetailsModal" 
              class="w-10 h-10 bg-gray-100 dark:bg-slate-800 rounded-full flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-slate-700 hover:text-gray-900 dark:hover:text-white transition-all duration-300"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Modal Content -->
        <div class="p-6" v-if="selectedOrder">
          <!-- Order Info -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-2xl p-6 border border-purple-200/50 dark:border-purple-700/50">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <svg class="w-5 h-5 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Информация о заказе
              </h3>
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Дата создания:</span>
                  <span class="font-medium text-gray-900 dark:text-white">{{ new Date(selectedOrder.created_at).toLocaleDateString('ru-RU', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  }) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Статус:</span>
                  <span 
                    :class="[
                      'px-3 py-1 text-sm font-semibold rounded-full',
                      getStatusColor(selectedOrder.status)
                    ]"
                  >
                    {{ getStatusText(selectedOrder.status) }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Общая сумма:</span>
                  <span class="text-xl font-bold text-purple-600 dark:text-purple-400">{{ selectedOrder.total_amount }} ₽</span>
                </div>
              </div>
            </div>

            <div class="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-2xl p-6 border border-green-200/50 dark:border-green-700/50">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <svg class="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Информация о товаре
              </h3>
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Название:</span>
                  <span class="font-medium text-gray-900 dark:text-white text-right">{{ selectedOrder.product.title }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Количество:</span>
                  <span class="font-medium text-gray-900 dark:text-white">{{ selectedOrder.quantity }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Цена за ед.:</span>
                  <span class="font-medium text-gray-900 dark:text-white">{{ selectedOrder.product.price }} ₽</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Product Details -->
          <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-200 dark:border-slate-700 p-6 mb-6">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Детали товара</h3>
            <div class="flex items-start space-x-6">
              <div class="w-32 h-32 rounded-2xl overflow-hidden bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-800 dark:to-blue-800 flex-shrink-0 shadow-lg">
                <img 
                  :src="selectedOrder.product.images && selectedOrder.product.images.length > 0 ? selectedOrder.product.images[0].image : (selectedOrder.product.image_url || noImage)" 
                  :alt="selectedOrder.product.title"
                  class="w-full h-full object-cover"
                  @error="(event) => { const target = event.target as HTMLImageElement; if (target) target.src = noImage; }"
                />
              </div>
              <div class="flex-1">
                <h4 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">{{ selectedOrder.product.title }}</h4>
                <p class="text-gray-600 dark:text-gray-400 mb-4 leading-relaxed">{{ selectedOrder.product.description }}</p>
                
                <!-- Download Link -->
                <div v-if="selectedOrder.product.download_link" class="mb-4">
                  <a 
                    :href="selectedOrder.product.download_link" 
                    target="_blank"
                    class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-medium hover:from-green-700 hover:to-emerald-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
                  >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Скачать товар
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Usage Instructions - только для оплаченных заказов -->
          <div v-if="selectedOrder.product.usage_instructions && (selectedOrder.status === 'paid' || selectedOrder.status === 'delivered')" class="bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 rounded-2xl border border-yellow-200/50 dark:border-yellow-700/50 p-6">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Инструкции по использованию
            </h3>
            <div class="prose prose-lg max-w-none dark:prose-invert" v-html="renderedUsageInstructions(selectedOrder.product.usage_instructions)"></div>
          </div>
          
          <!-- Информация для отклоненных заказов -->
          <div v-if="selectedOrder.status === 'seller_rejected' || selectedOrder.status === 'payment_rejected'" class="bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20 rounded-2xl border border-red-200/50 dark:border-red-700/50 p-6">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Почему так могло получиться?
            </h3>
            <div class="space-y-3 text-gray-700 dark:text-gray-300">
              <div v-if="selectedOrder.status === 'seller_rejected'" class="p-4 bg-red-100 dark:bg-red-900/30 rounded-lg border-l-4 border-red-500">
                <p class="font-medium text-red-800 dark:text-red-200 mb-2">Заказ отклонен продавцом</p>
                <p class="text-sm">Возможные причины:</p>
                <ul class="list-disc list-inside mt-2 text-sm space-y-1">
                  <li>Товар временно недоступен</li>
                  <li>Проблемы с оплатой</li>
                  <li>Технические сложности</li>
                  <li>Недостаточная информация в заказе</li>
                </ul>
                <p class="mt-3 text-sm font-medium">Рекомендуем связаться с продавцом для уточнения деталей.</p>
              </div>
              
              <div v-if="selectedOrder.status === 'payment_rejected'" class="p-4 bg-red-100 dark:bg-red-900/30 rounded-lg border-l-4 border-red-500">
                <p class="font-medium text-red-800 dark:text-red-200 mb-2">Платеж отклонен платежной системой</p>
                <p class="text-sm">Возможные причины:</p>
                <ul class="list-disc list-inside mt-2 text-sm space-y-1">
                  <li>Недостаточно средств на карте</li>
                  <li>Банк заблокировал операцию</li>
                  <li>Проблемы с 3D Secure</li>
                  <li>Технические сбои платежной системы</li>
                </ul>
                <p class="mt-3 text-sm font-medium">Попробуйте повторить оплату или используйте другую карту.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Line clamp utilities */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.8);
}

/* Animation delays for staggered animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: fadeInUp 0.6s ease-out forwards;
}

.slide-in-from-top-2 {
  animation: slideInFromTop 0.5s ease-out forwards;
}

@keyframes slideInFromTop {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
