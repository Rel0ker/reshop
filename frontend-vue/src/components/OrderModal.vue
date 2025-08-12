<template>
  <div v-if="isVisible" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
    <div class="bg-slate-800/95 backdrop-blur-md border border-purple-500/50 rounded-2xl p-8 shadow-2xl max-w-md w-full relative text-white transform transition-all duration-300">
      <!-- Close Button -->
      <button @click="close" class="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl transition-colors duration-200">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Header -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          Оформление заказа
        </h2>
        <p class="text-gray-400">Заполните форму для покупки товара</p>
      </div>

      <!-- Product Info -->
      <div v-if="product" class="mb-8 p-4 bg-white/5 rounded-xl border border-white/10">
        <h3 class="text-xl font-semibold mb-2 text-white">{{ product.title }}</h3>
        <p class="text-2xl font-bold text-purple-400">{{ product.price }} ₽</p>
      </div>

      <!-- Order Form -->
      <form @submit.prevent="submitOrder" class="space-y-6">
        <div>
          <label for="email" class="block text-gray-300 text-sm font-semibold mb-2">
            Email для чека
          </label>
          <input
            type="email"
            id="email"
            v-model="orderForm.email"
            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
            placeholder="your@email.com"
            required
          />
        </div>

        <div>
          <label for="quantity" class="block text-gray-300 text-sm font-semibold mb-2">
            Количество
          </label>
          <input
            type="number"
            id="quantity"
            v-model.number="orderForm.quantity"
            min="1"
            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
            required
          />
        </div>

        <div>
          <label for="comment" class="block text-gray-300 text-sm font-semibold mb-2">
            Комментарий для продавца
            <span class="text-gray-500 text-xs">(необязательно)</span>
          </label>
          <textarea
            id="comment"
            v-model="orderForm.comment"
            rows="3"
            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 resize-none"
            placeholder="Ваши пожелания или вопросы..."
          ></textarea>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-4 px-6 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <span v-if="!isSubmitting" class="flex items-center justify-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            Оформить заказ
          </span>
          <span v-else class="flex items-center justify-center gap-2">
            <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Оформляем...
          </span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, reactive, watch } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api';
import { useAuth } from '../store';

interface Product {
  id: string;
  title: string;
  price: string;
}

const props = defineProps({
  isVisible: {
    type: Boolean,
    required: true,
  },
  product: {
    type: Object as () => Product | null,
    default: null,
  },
});

const emit = defineEmits(['close', 'orderSuccess']);

const auth = useAuth();

const router = useRouter();

const orderForm = reactive({
  email: auth.user?.email || '',
  quantity: 1,
  comment: '',
});

const isSubmitting = ref(false);

watch(() => auth.user?.email, (newEmail) => {
  if (newEmail) {
    orderForm.email = newEmail;
  }
}, { immediate: true });

const close = () => {
  emit('close');
};

const submitOrder = async () => {
  if (!props.product) return;

  isSubmitting.value = true;
  
  try {
    const paymentData = {
      product: props.product.id,
      quantity: orderForm.quantity,
      comment: orderForm.comment,
      receipt_email: orderForm.email,
    };
    
    console.log('Sending payment request to /payments/ with data:', paymentData);
    const response = await api.post('/payments/', paymentData);
    console.log('Payment initiated successfully:', response.data);
    
    // Проверяем различные варианты URL для подтверждения
    const confirmationUrl = response.data.payment_url || response.data.confirmation_url;
    const paymentId = response.data.payment_id;
    const orderId = response.data.id;
    
    console.log('Payment details:', {
      confirmationUrl,
      paymentId,
      orderId,
      fullResponse: response.data
    });
    
    if (confirmationUrl) {
      console.log('Redirecting to payment confirmation:', confirmationUrl);
      window.location.href = confirmationUrl;
    } else if (paymentId) {
      // Если есть ID платежа, но нет URL, перенаправляем на страницу успеха
      console.log('Payment created but no confirmation URL, redirecting to success page');
      router.push({ path: '/order-success', query: { order_id: orderId } });
    } else {
      // Если нет ни URL, ни ID платежа
      console.warn('No payment confirmation URL or payment ID found');
      alert('Платеж успешно создан, но URL подтверждения или ID заказа не найдены.');
      emit('orderSuccess');
      close();
    }
  } catch (error: any) {
    console.error('Error initiating payment:', error);
    
    let errorMessage = 'Ошибка при инициировании платежа. Пожалуйста, попробуйте еще раз.';
    
    if (error.response?.data?.error) {
      errorMessage = error.response.data.error;
    } else if (error.response?.status === 500) {
      errorMessage = 'Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.';
    } else if (error.response?.status === 400) {
      errorMessage = 'Неверные данные запроса. Проверьте введенную информацию.';
    }
    
    alert(errorMessage);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* Add any specific styles for the modal here */
</style>