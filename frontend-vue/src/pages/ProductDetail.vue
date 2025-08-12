<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <div class="container mx-auto px-4 py-8">
      <!-- Back Button -->
      <div class="mb-6">
        <button
          @click="goBack"
          class="group flex items-center gap-3 px-6 py-3 bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 hover:from-gray-200 hover:to-gray-300 dark:hover:from-gray-600 dark:hover:to-gray-700 text-gray-700 dark:text-white rounded-xl transition-all duration-300 border border-gray-200 dark:border-gray-600 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
        >
          <svg class="w-5 h-5 group-hover:-translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
          <span class="font-medium">Назад к каталогу</span>
          <div class="w-2 h-2 bg-purple-500 rounded-full opacity-0 group-hover:opacity-100 transition-all duration-300 group-hover:animate-pulse"></div>
        </button>
      </div>
      
      <!-- Page Header -->
      <div class="text-center mb-8 animate-fade-in">
        <div class="relative">
          <div class="absolute inset-0 bg-gradient-to-r from-purple-400/20 via-pink-400/20 to-rose-400/20 dark:from-purple-600/20 dark:via-pink-600/20 dark:to-rose-600/20 rounded-full blur-3xl"></div>
          <h1 class="relative text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 animate-gradient">
              Детали товара
            </span>
          </h1>
        </div>
        <p class="text-xl text-gray-600 dark:text-gray-300 mb-2">
          Подробная информация о выбранном товаре
        </p>
      </div>
      
      <!-- Product Content -->
      <div v-if="product" class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-2xl shadow-xl backdrop-blur-sm animate-fade-in stagger-1 overflow-hidden">
        <div class="p-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Product Images -->
            <div class="animate-fade-in stagger-2">
              <div class="relative overflow-hidden rounded-lg mb-4 bg-gray-100 dark:bg-gray-800 product-image-container">
                <img 
                  v-if="hasMainImage"
                  :src="mainImage" 
                  alt="Product Main Image" 
                  class="w-full aspect-square object-cover transition-transform duration-500 hover:scale-105 product-image" 
                />
                <ProductImagePlaceholder 
                  v-else
                  class="w-full aspect-square"
                  text="Фото товара"
                  subtitle="Изображение не загружено"
                />
                
                <!-- Overlay Badges on Image -->
                <div class="absolute top-4 left-4 flex flex-col gap-3">
                  <!-- Status Badge -->
                  <div class="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400 text-sm font-medium rounded-full border border-green-200 dark:border-green-800 backdrop-blur-sm">
                    <span class="w-2 h-2 bg-green-500 rounded-full inline-block mr-2 animate-pulse"></span>
                    В наличии
                  </div>
                  
                  <!-- Rating Badge -->
                  <div v-if="product.seller_rating" class="px-3 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400 text-sm font-medium rounded-full border border-yellow-200 dark:border-yellow-800 backdrop-blur-sm">
                    <span class="text-yellow-600">⭐</span>
                    {{ product.seller_rating }}/5
                  </div>
                </div>
                
                <!-- Hover Overlay -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
              </div>
              
              <!-- Thumbnail Images -->
              <div v-if="product.images && product.images.length > 1" class="flex space-x-2 overflow-x-auto">
                <img
                  v-for="(image, index) in product.images"
                  :key="index"
                  :src="image.image"
                  @click="setMainImage(image.image)"
                  :class="[
                    'w-20 h-20 object-cover rounded-md cursor-pointer border-2 transition-all duration-300 hover:scale-110',
                    mainImage === image.image
                      ? 'border-purple-500 dark:border-pink-500 shadow-lg shadow-purple-500/25'
                      : 'border-transparent hover:border-purple-500 dark:hover:border-pink-500'
                  ]"
                />
              </div>
            </div>

            <!-- Product Details -->
            <div class="animate-fade-in stagger-3">
              <h1 class="text-3xl font-bold mb-4 text-gray-900 dark:text-white leading-tight">{{ product.title }}</h1>
              
              <!-- Product Meta Info -->
              <div class="mb-6 space-y-4">
                <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-2 h-2 bg-purple-500 rounded-full"></span>
                  <span>ID товара: {{ product.id }}</span>
                </div>
                
                <!-- Seller Information Card -->
                <div class="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl p-4 border border-blue-200 dark:border-blue-800/30">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                      </div>
                      <div>
                        <h3 class="font-semibold text-gray-900 dark:text-white">Продавец</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400">{{ product.seller.email }}</p>
                      </div>
                    </div>
                    
                    <!-- Seller Rating Badge -->
                    <div v-if="product.seller_rating" class="text-right">
                      <div class="inline-flex items-center gap-2 px-3 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400 text-sm font-medium rounded-full border border-yellow-200 dark:border-yellow-800">
                        <svg class="w-4 h-4 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                        </svg>
                        <span>{{ product.seller_rating }}/5</span>
                      </div>
                    </div>
                    
                    <div v-else class="text-right">
                      <div class="inline-flex items-center gap-2 px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-sm font-medium rounded-full border border-gray-200 dark:border-gray-600">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <span>Нет оценок</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Seller Stats - Only show if we have real data -->
                  <div v-if="product.seller_rating" class="mt-4 pt-4 border-t border-blue-200 dark:border-blue-800/30">
                    <div class="text-center">
                      <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">Статистика продавца</div>
                      <div class="flex items-center justify-center gap-1">
                        <span class="text-sm text-gray-500 dark:text-gray-400">Средняя оценка:</span>
                        <div class="flex items-center gap-1">
                          <svg v-for="star in 5" :key="star" 
                               class="w-4 h-4" 
                               :class="star <= product.seller_rating ? 'text-yellow-400 fill-current' : 'text-gray-300 dark:text-gray-600'"
                               fill="currentColor" 
                               viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                          </svg>
                          <span class="font-semibold text-gray-900 dark:text-white">{{ product.seller_rating }}/5</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Buy Button -->
              <div class="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl p-6 border border-purple-200 dark:border-purple-800/30">
                <div class="text-center mb-6">
                  <div class="text-4xl font-bold text-purple-600 dark:text-pink-500 mb-2">{{ product.price }} ₽</div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">Цена товара</div>
                </div>
                
                <button
                  @click="openOrderModal"
                  :disabled="product.quantity === 0"
                  :class="[
                    'w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 disabled:transform-none disabled:cursor-not-allowed',
                    product.quantity > 0
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-600/25'
                      : 'bg-gray-400 text-gray-200 cursor-not-allowed'
                  ]"
                >
                  {{ product.quantity > 0 ? 'Купить сейчас' : 'Нет в наличии' }}
                </button>
                
                <div class="mt-4 text-center">
                  <div class="text-sm text-gray-600 dark:text-gray-400">
                    В наличии: <span class="font-semibold text-purple-600 dark:text-pink-500">{{ product.quantity }}</span> шт.
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Product Description -->
          <div class="mt-8 animate-fade-in stagger-4">
            <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Описание товара</h2>
            <div class="prose prose-lg dark:prose-invert max-w-none" v-html="renderedDescription"></div>
          </div>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-16">
          <div class="max-w-md mx-auto">
            <div class="relative mb-8">
              <div class="w-24 h-24 border-4 border-purple-200 dark:border-purple-800 rounded-full mx-auto"></div>
              <div class="absolute inset-0 w-24 h-24 border-4 border-purple-600 border-t-transparent rounded-full mx-auto animate-spin"></div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Загрузка товара</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">Пожалуйста, подождите...</p>
            <div class="flex justify-center gap-2">
              <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
        
        <!-- Error State -->
        <div v-if="!loading && !product" class="text-center py-16">
          <div class="max-w-md mx-auto">
            <div class="relative mb-8">
              <div class="w-24 h-24 bg-gradient-to-r from-red-100 to-pink-100 dark:from-red-900/30 dark:to-pink-900/30 rounded-full mx-auto flex items-center justify-center">
                <span class="text-4xl">❌</span>
              </div>
              <div class="absolute inset-0 w-24 h-24 bg-gradient-to-r from-red-500 to-pink-500 rounded-full mx-auto opacity-20 animate-pulse"></div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Товар не найден</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">Произошла ошибка при загрузке товара</p>
            <button
              @click="goBack"
              class="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg transition-all duration-300 transform hover:scale-105"
            >
              Вернуться к каталогу
            </button>
          </div>
        </div>

        <!-- Comments Section -->
        <div v-if="product" class="mt-12 animate-fade-in stagger-3">
          <div class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-2xl p-8 shadow-xl backdrop-blur-sm">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                  </svg>
                </div>
                Отзывы и комментарии
                <span class="text-sm text-gray-500 dark:text-gray-400">({{ comments.length }})</span>
              </h2>
            </div>

            <!-- Add Comment Form - только для купивших товар -->
            <div v-if="isAuthenticated && hasPurchased" class="mb-8 p-6 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-800 dark:to-blue-900/20 rounded-xl border border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Добавить комментарий</h3>
              <form @submit.prevent="addComment" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Ваш отзыв</label>
                  <textarea
                    v-model="newComment.text"
                    rows="4"
                    class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 dark:focus:ring-pink-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white resize-none"
                    placeholder="Поделитесь своими впечатлениями о товаре..."
                    required
                  ></textarea>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Оценка (необязательно)</label>
                  <div class="flex items-center gap-2">
                    <div v-for="star in 5" :key="star" class="flex items-center">
                      <input
                        type="radio"
                        :id="`star-${star}`"
                        :value="star"
                        v-model="newComment.rating"
                        class="sr-only"
                      />
                      <label
                        :for="`star-${star}`"
                        class="cursor-pointer text-2xl transition-colors duration-200"
                        :class="[
                          star <= (newComment.rating || 0)
                            ? 'text-yellow-400'
                            : 'text-gray-300 dark:text-gray-600 hover:text-yellow-300'
                        ]"
                      >
                        ★
                      </label>
                    </div>
                    <span class="text-sm text-gray-500 dark:text-gray-400 ml-2">
                      {{ newComment.rating || 0 }}/5
                    </span>
                  </div>
                </div>
                
                <button
                  type="submit"
                  :disabled="submittingComment"
                  class="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-400 disabled:to-gray-500 text-white rounded-lg transition-all duration-300 transform hover:scale-105 disabled:transform-none"
                >
                  <div v-if="submittingComment" class="flex items-center gap-2">
                    <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Отправка...</span>
                  </div>
                  <div v-else class="flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                    </svg>
                    <span>Отправить комментарий</span>
                  </div>
                </button>
              </form>
            </div>

            <!-- Сообщение для не купивших товар -->
            <div v-else-if="isAuthenticated && !hasPurchased" class="mb-8 p-6 bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-xl border border-amber-200 dark:border-amber-700">
              <div class="flex items-center gap-3 text-amber-800 dark:text-amber-200">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <div>
                  <h3 class="text-lg font-semibold">Оставить отзыв можно только после покупки</h3>
                  <p class="text-sm mt-1">Купите товар, чтобы поделиться своими впечатлениями с другими покупателями</p>
                </div>
              </div>
            </div>

            <!-- Сообщение для неавторизованных пользователей -->
            <div v-else-if="!isAuthenticated" class="mb-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl border border-blue-200 dark:border-blue-700">
              <div class="flex items-center gap-3 text-blue-800 dark:text-blue-200">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div>
                  <h3 class="text-lg font-semibold">Войдите в систему, чтобы оставить отзыв</h3>
                  <p class="text-sm mt-1">Авторизуйтесь и купите товар, чтобы поделиться своими впечатлениями</p>
                </div>
              </div>
            </div>

            <!-- Comments List -->
            <div v-if="comments.length > 0" class="space-y-6">
              <div
                v-for="comment in comments"
                :key="comment.id"
                class="p-6 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700"
              >
                <div class="flex items-start justify-between mb-3">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                      <span class="text-white font-semibold text-sm">
                        {{ comment.user.email.charAt(0).toUpperCase() }}
                      </span>
                    </div>
                    <div>
                      <div class="font-medium text-gray-900 dark:text-white">
                        {{ comment.user.email }}
                      </div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">
                        {{ formatDate(comment.created_at) }}
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="comment.rating" class="flex items-center gap-1">
                    <div v-for="star in 5" :key="star" class="text-sm">
                      <span :class="star <= comment.rating ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600'">★</span>
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400 ml-1">{{ comment.rating }}/5</span>
                  </div>
                </div>
                
                <div class="text-gray-700 dark:text-gray-300 leading-relaxed">
                  {{ comment.text }}
                </div>
              </div>
            </div>

            <!-- No Comments -->
            <div v-else class="text-center py-12">
              <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Пока нет комментариев</h3>
              <p class="text-gray-500 dark:text-gray-400">
                {{ isAuthenticated ? 'Будьте первым, кто оставит отзыв!' : 'Войдите, чтобы оставить комментарий' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Order Modal -->
        <OrderModal
          :isVisible="isOrderModalVisible"
          :product="product"
          @close="closeOrderModal"
          @orderSuccess="handleOrderSuccess"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { marked } from 'marked';
import { useRoute, useRouter } from 'vue-router';
import { api } from '../api';
import noImage from '../assets/no-image.png';
import OrderModal from '../components/OrderModal.vue';

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
  seller: Seller;
  images: ProductImage[];
  usage_instructions?: string;
  seller_rating?: number;
  comments?: ProductComment[];
  quantity: number; // Added quantity to the Product interface
}

interface ProductComment {
  id: string;
  user: {
    id: string;
    email: string;
  };
  text: string;
  rating?: number;
  created_at: string;
  updated_at: string;
}

const route = useRoute();
const router = useRouter();
const product = ref<Product | null>(null);
const loading = ref(true);
const mainImage = ref(noImage);
const isOrderModalVisible = ref(false);
const hasPurchased = ref(false);
const comments = ref<ProductComment[]>([]);
const newComment = ref({
  text: '',
  rating: 0
});
const submittingComment = ref(false);
const isAuthenticated = ref(false);

const goBack = () => {
  router.push('/popular');
};

const fetchProduct = async (id: string) => {
  loading.value = true;
  try {
    const response = await api.get(`/products/${id}/`);
    product.value = response.data;
    if (product.value && product.value.images && product.value.images.length > 0) {
      mainImage.value = product.value.images[0].image;
    } else {
      mainImage.value = noImage;
    }
    
    // Загружаем комментарии для товара
    await fetchComments(id);
    await checkPurchaseStatus(id);
  } catch (error: any) {
    console.error('Ошибка при загрузке товара:', error);
    if (error.response) {
      console.error('Данные ошибки:', error.response.data);
      console.error('Статус ошибки:', error.response.status);
      console.error('Заголовки ошибки:', error.response.headers);
    } else if (error.request) {
      console.error('Запрос ошибки:', error.request);
    } else {
      console.error('Сообщение ошибки:', error.message);
    }
    product.value = null;
  } finally {
    loading.value = false;
  }
};

const setMainImage = (imageSrc: string) => {
  mainImage.value = imageSrc;
};

const openOrderModal = () => {
  isOrderModalVisible.value = true;
};

const closeOrderModal = () => {
  isOrderModalVisible.value = false;
};

const handleOrderSuccess = () => {
  // Optionally, add logic after a successful order, e.g., show a success message
  console.log('Order placed successfully!');
  // Проверяем статус покупки после успешного заказа
  if (product.value) {
    checkPurchaseStatus(product.value.id);
  }
};

const fetchComments = async (productId: string) => {
  try {
    const response = await api.get(`/comments/?product_id=${productId}`);
    comments.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке комментариев:', error);
  }
};

const checkPurchaseStatus = async (productId: string) => {
  if (!isAuthenticated.value) {
    hasPurchased.value = false;
    return;
  }
  
  try {
    const response = await api.get(`/products/${productId}/has_purchased/`);
    hasPurchased.value = response.data.has_purchased;
  } catch (error) {
    console.error('Ошибка при проверке статуса покупки:', error);
    hasPurchased.value = false;
  }
};

const addComment = async () => {
  if (!product.value || !newComment.value.text.trim()) return;
  
  submittingComment.value = true;
  try {
    const response = await api.post('/comments/', {
      product: product.value.id,
      text: newComment.value.text.trim(),
      rating: newComment.value.rating || null
    });
    
    // Добавляем новый комментарий в список
    comments.value.unshift(response.data);
    
    // Очищаем форму
    newComment.value.text = '';
    newComment.value.rating = 0;
    
    console.log('Комментарий добавлен успешно!');
  } catch (error) {
    console.error('Ошибка при добавлении комментария:', error);
  } finally {
    submittingComment.value = false;
  }
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const checkAuthStatus = () => {
  const token = localStorage.getItem('access_token');
  isAuthenticated.value = !!token;
};

const renderedDescription = computed(() => {
  return marked(product.value?.description || '', { gfm: true });
});

const renderedUsageInstructions = computed(() => {
  return marked(product.value?.usage_instructions || '', { gfm: true });
});

const hasMainImage = computed(() => {
  return mainImage.value !== noImage;
});

onMounted(() => {
  checkAuthStatus();
  if (route.params.id) {
    fetchProduct(route.params.id as string);
  }
});

watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchProduct(newId as string);
  }
});
</script>

<style scoped>
/* Add any specific styles for this component here */
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

@keyframes gradient {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(147, 51, 234, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(147, 51, 234, 0.6);
  }
}

.animate-fade-in {
  animation: fadeIn 0.8s ease-out;
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite;
}

/* Smooth transitions for all elements */
* {
  transition: all 0.3s ease;
}

/* Custom scrollbar for image thumbnails */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #c084fc;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #a855f7;
}

/* Dark mode scrollbar */
.dark .overflow-x-auto::-webkit-scrollbar-track {
  background: #334155;
}

.dark .overflow-x-auto::-webkit-scrollbar-thumb {
  background: #ec4899;
}

.dark .overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #db2777;
}

/* Hover effects for product images */
.product-image-container:hover .product-image {
  transform: scale(1.05);
}

/* Staggered animation for elements */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
.stagger-4 { animation-delay: 0.4s; }
.stagger-5 { animation-delay: 0.5s; }
.stagger-6 { animation-delay: 0.6s; }

/* Glass morphism effect */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.dark .glass {
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Enhanced button hover effects */
.btn-hover {
  position: relative;
  overflow: hidden;
}

.btn-hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-hover:hover::before {
  left: 100%;
}
</style>