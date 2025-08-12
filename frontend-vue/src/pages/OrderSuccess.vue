<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
    <div class="bg-gray-800 p-8 rounded-lg shadow-lg text-center max-w-md w-full">
      <svg class="w-24 h-24 text-green-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <h1 class="text-3xl font-bold text-green-600 mb-4">Оплата прошла успешно!</h1>
      <img v-if="product?.images && product.images.length > 0" :src="product.images[0].image" alt="Product Image" class="w-48 aspect-square object-cover rounded-lg mx-auto mb-6" />
      <img v-else :src="noImage" alt="No Image" class="w-48 aspect-square object-cover rounded-lg mx-auto mb-6" />
    <p class="text-lg text-gray-700 mb-6">
      Ваш заказ успешно оформлен. Спасибо за покупку!
    </p>

    <div v-if="isLoading" class="text-gray-400">Loading order details...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else-if="orderDetails" class="text-left w-full mt-6">
      <p class="text-lg text-gray-300 mb-2">
        Идентификатор заказа: <span class="font-semibold text-white">{{ orderDetails.id }}</span>
      </p>
      <p class="text-lg text-gray-300 mb-4">
        Общая стоимость: <span class="font-semibold text-white">{{ orderDetails.total_amount }}</span>
      </p>
      <h2 class="text-xl font-bold text-white mb-3">Состав заказа:</h2>
      <div v-for="item in orderDetails.items" :key="item.product_name" class="mb-4 p-2 border border-gray-700 rounded-md">
         <div class="flex items-center space-x-4">
           <img v-if="item.image_url" :src="item.image_url" alt="Product Image" class="w-16 h-16 object-cover rounded-md"/>
           <img v-else :src="noImage" alt="No Image" class="w-16 h-16 object-cover rounded-md"/>
           <div class="flex-1">
             <p class="text-lg font-semibold text-white">{{ truncateText(item.product_name, 50) }} (x{{ item.quantity }}) - {{ item.price }}</p>
             <p v-if="item.description" class="text-sm text-gray-400">{{ truncateText(item.description, 50) }}</p>
             <p v-if="item.seller_info" class="text-sm text-gray-400">Продавец: {{ item.seller_info }}</p>
             <p v-if="item.usage_instructions" class="text-sm text-gray-400">Инструкция по активации: {{ item.usage_instructions }}</p>
           </div>
         </div>
       </div>
    </div>

    <router-link
      to="/buyer"
      class="mt-8 inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      В личный кабинет
    </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { api } from '../api'; // Убедитесь, что путь к api.ts правильный
import noImage from '../assets/no-image.png';

interface OrderItem {
  product_name: string;
  quantity: number;
  price: number;
  seller_info?: string; // Добавляем опциональное поле
  image_url?: string; // Добавляем опциональное поле
  usage_instructions?: string; // Добавляем опциональное поле для инструкции по использованию
  description?: string; // Добавляем опциональное поле для описания
}

interface OrderDetails {
  id: string;
  total_amount: string;
  items: OrderItem[];
  // Добавьте другие поля заказа, если они нужны
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
/* Стили для этой страницы */
</style>