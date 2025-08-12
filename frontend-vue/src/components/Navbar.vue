<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xl border-b border-gray-200/50 dark:border-slate-700/50 shadow-lg">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-3 group">
          <div class="relative">
            <img src="/logo.svg" alt="Re:shop Logo" class="w-10 h-10 rounded-sm group-hover:scale-110 transition-all duration-500" />
            
          </div>
          <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 bg-clip-text text-transparent">
            Re:shop
          </span>
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link
            to="/popular"
            class="relative text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-all duration-300 group"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/popular' }"
          >
            Каталог
            <span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-primary-600 to-secondary-600 group-hover:w-full transition-all duration-300"></span>
            <span v-if="$route.path === '/popular'" class="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary-600 to-secondary-600"></span>
          </router-link>
          <router-link
            to="/blog"
            class="relative text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-all duration-300 group"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/blog' }"
          >
            Блог
            <span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-primary-600 to-secondary-600 group-hover:w-full transition-all duration-300"></span>
            <span v-if="$route.path === '/blog'" class="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary-600 to-secondary-600"></span>
          </router-link>
          <router-link
            to="/support"
            class="relative text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-all duration-300 group"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/support' }"
          >
            Поддержка
            <span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-primary-600 to-secondary-600 group-hover:w-full transition-all duration-300"></span>
            <span v-if="$route.path === '/support'" class="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary-600 to-secondary-600"></span>
          </router-link>
        </div>

        <!-- Animated Search Bar (Desktop) -->
        <div class="hidden md:block mx-8 px-4" data-search>
          <!-- Vue поле ввода -->
          <div class="relative group transition-all duration-500 ease-out ">
            <input class="pr-10"
              v-model="searchQuery"
              type="text"
              :placeholder="getPlaceholder()"
              :class="getInputClasses()"
              @input="handleSearchInput"
              @focus="isSearchFocused = true"
              @blur="isSearchFocused = false"
              @keydown.enter="handleSearch"
            />
            
            <!-- Кнопка поиска -->
            <button 
              @click="handleSearch"
              class="absolute right-1 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center hover:bg-purple-700 transition-all duration-300"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
          
          <!-- Dropdown с результатами поиска -->
          <div v-if="searchQuery && (isSearchFocused || searchResults.length > 0)"
               class="absolute top-full left-1/2 w-full max-w-md mt-3 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-2xl shadow-2xl z-50 overflow-hidden transform -translate-x-1/2 transition-all duration-500 ease-out animate-in slide-in-from-top-2">
            <!-- Заголовок -->
            <div class="px-4 py-3 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 border-b border-gray-200 dark:border-slate-600">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Результаты поиска</span>
                <span class="text-xs text-gray-500 dark:text-gray-400">{{ searchResults.length }} найдено</span>
              </div>
            </div>
            
            <div class="max-h-80 overflow-y-auto">
              <!-- Состояние загрузки -->
              <div v-if="isSearching" class="p-8 text-center">
                <div class="text-gray-500 dark:text-gray-400">
                  <div class="inline-flex items-center gap-3 mb-3">
                    <div class="w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                    <span class="font-medium text-gray-700 dark:text-gray-300">Идет поиск...</span>
                  </div>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Находим лучшие товары для вас</p>
                </div>
              </div>
              
              <!-- Результаты -->
              <div v-else-if="searchResults.length > 0">
                <div v-for="(product, index) in searchResults" :key="product.id" 
                     @click="selectSearchResult(product)" 
                     class="group p-4 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 cursor-pointer transition-all duration-300 border-b border-gray-100 dark:border-slate-600 last:border-b-0 transform hover:scale-[1.02] hover:translate-x-1"
                     :style="{ animationDelay: `${index * 100}ms` }">
                  
                  <div class="flex items-start gap-3">
                    <!-- Изображение товара -->
                    <div class="w-12 h-12 rounded-xl overflow-hidden bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-800 dark:to-pink-800 flex-shrink-0 shadow-sm">
                      <img 
                        :src="product.images && product.images.length > 0 ? product.images[0].image : (product.image_url || '/no-image.png')" 
                        :alt="product.title"
                        class="w-full h-full object-cover"
                        @error="(event) => { const target = event.target as HTMLImageElement; if (target) target.src = '/no-image.png'; }"
                      />
                    </div>
                    
                    <!-- Информация о товаре -->
                    <div class="flex-1 min-w-0">
                      <h4 class="font-semibold text-gray-900 dark:text-white text-sm leading-tight mb-1 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors line-clamp-2">
                        {{ product.title }}
                      </h4>
                      <p class="text-xs text-gray-500 dark:text-gray-400 line-clamp-1 mb-2">
                        {{ product.description }}
                      </p>
                      
                      <!-- Цена и статус -->
                      <div class="flex items-center justify-between">
                        <span class="text-lg font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                          {{ product.price }} ₽
                        </span>
                        <span :class="[
                          'px-3 py-1.5 rounded-full text-xs font-semibold shadow-sm',
                          product.quantity > 0 
                            ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                            : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                        ]">
                          {{ product.quantity > 0 ? 'В наличии' : 'Нет в наличии' }}
                        </span>
                      </div>
                    </div>
                    
                    <!-- Иконка перехода -->
                    <div class="w-5 h-5 text-gray-400 group-hover:text-purple-500 transition-colors flex-shrink-0 transform group-hover:translate-x-1">
                      <svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
                
                <!-- Кнопка "Показать все" -->
                <div class="p-3 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 border-t border-gray-200 dark:border-slate-600">
                  <button
                    @click="handleSearch"
                    class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    Показать все результаты для "{{ searchQuery }}"
                  </button>
                </div>
              </div>
              
              <!-- Ничего не найдено -->
              <div v-else-if="searchQuery.length >= 2" class="p-8 text-center">
                <div class="text-gray-500 dark:text-gray-400">
                  <div class="text-6xl mb-4 animate-bounce">🔍</div>
                  <p class="font-medium mb-2 text-gray-700 dark:text-gray-300">Ничего не найдено</p>
                  <p class="text-sm">Попробуйте изменить запрос</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side -->
        <div class="flex items-center space-x-4">
          <!-- Search Button (Mobile) -->
          <button
            @click="toggleSearch"
            class="md:hidden w-10 h-10 bg-gray-100 dark:bg-slate-800 rounded-full flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-slate-700 transition-all duration-300 hover:scale-110"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>

          <!-- User Menu -->
          <div v-if="isAuthenticated" class="relative" data-user-menu>
            <button
              @click="toggleUserMenu"
              @mouseenter="openUserMenu"
              @mouseleave="closeUserMenu"
              class="flex items-center space-x-2 p-2 rounded-2xl hover:bg-gray-100 dark:hover:bg-slate-800 transition-all duration-300 hover:scale-105"
            >
              <div class="relative">
                <div class="w-8 h-8 bg-gradient-to-br from-primary-500 via-secondary-500 to-tertiary-500 rounded-full flex items-center justify-center shadow-lg">
                  <span class="text-white text-sm font-bold">
                    {{ userInitial }}
                  </span>
                </div>
              
              </div>
              <svg class="w-4 h-4 text-gray-600 dark:text-gray-400 transition-transform duration-300" :class="{ 'rotate-180': isUserMenuOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- User Dropdown -->
            <transition
              enter-active-class="transition ease-out duration-300"
              enter-from-class="opacity-0 scale-95 translate-y-2"
              enter-to-class="opacity-100 scale-100 translate-y-0"
              leave-active-class="transition ease-in duration-500"
              leave-from-class="opacity-100 scale-100 translate-y-0"
              leave-to-class="opacity-0 scale-95 translate-y-2"
            >
              <div
                v-if="isUserMenuOpen"
                @mouseenter="openUserMenu"
                @mouseleave="closeUserMenu"
                class="absolute right-0 mt-3 py-2 w-56 bg-white dark:bg-slate-800 backdrop-blur-2xl rounded-lg  shadow-2xl border border-gray-200/50 dark:border-slate-700/50  z-50"
              >
                <div class="px-4 pb-3 border-b border-gray-100 dark:border-slate-700">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ user?.email }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ user?.role === 'seller' ? 'Продавец' : 'Покупатель' }}</p>
                </div>
                <router-link
                  :to="user?.role === 'seller' ? '/seller' : '/buyer'"
                  class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 transition-all duration-200"
                >
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  {{ user?.role === 'seller' ? 'Мои товары' : 'Мои заказы' }}
                </router-link>
                <router-link
                  to="/settings"
                  class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 transition-all duration-200"
                >
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Настройки
                </router-link>
                <div class="border-t border-gray-100 dark:border-slate-700 mt-2 pt-2">
                  <button
                    @click="logout"
                    class="flex items-center w-full px-4 py-3 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200"
                  >
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Выйти
                  </button>
                </div>
              </div>
            </transition>
          </div>
          
          <!-- Auth Buttons -->
          <div v-else class="flex items-center space-x-3">
            <router-link
              to="/login"
              class="px-4 py-2 text-purple-600 dark:text-purple-400 font-medium hover:text-purple-700 dark:hover:text-purple-300 transition-all duration-300 hover:scale-105"
            >
              Войти
            </router-link>
            <router-link
              to="/register"
              class="relative px-6 py-2 bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 text-white font-medium rounded-2xl hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 overflow-hidden group"
            >
              <span class="relative z-10">Регистрация</span>
              <div class="absolute inset-0 bg-gradient-to-r from-purple-700 via-pink-700 to-rose-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link>
          </div>
        </div>

          <!-- Mobile Menu Button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden w-10 h-10 bg-gray-100 dark:bg-slate-800 rounded-full flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-slate-700 transition-all duration-300 hover:scale-110"
            data-mobile-menu
          >
            <svg class="w-5 h-5 transition-transform duration-300" :class="{ 'rotate-90': isMobileMenuOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Search Bar -->
      <transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 -translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-4"
      >
        <div
          v-if="isSearchOpen"
          class="md:hidden pb-4"
          data-search
        >
          <div class="relative group transition-all duration-500 ease-out">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="getPlaceholder()"
                :class="getMobileInputClasses()"
                @input="handleSearchInput"
                @focus="isSearchFocused = true"
                @blur="isSearchFocused = false"
                @keydown.enter="handleSearch"
              />
              <!-- Clear button for mobile -->
              <button 
                v-if="searchQuery"
                @click="clearSearch"
                class="absolute right-12 top-1/2 transform -translate-y-1/2 w-6 h-6 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <div class="absolute inset-0 bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-rose-500/10 rounded-2xl opacity-0 focus-within:opacity-100 transition-opacity duration-500"></div>
              <button class="absolute right-1 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-full flex items-center justify-center hover:scale-110 transition-transform duration-200 shadow-lg" @click="handleSearch">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
            <!-- Mobile search suggestions -->
            <transition
              enter-active-class="transition ease-out duration-500"
              enter-from-class="opacity-0 scale-95 translate-y-2"
              enter-to-class="opacity-100 scale-100 translate-y-0"
              leave-active-class="transition ease-in duration-400"
              leave-from-class="opacity-100 scale-100 translate-y-0"
              leave-to-class="opacity-0 scale-95 translate-y-2"
            >
              <div 
                v-if="searchQuery"
                class="absolute top-full left-0 right-0 mt-3 bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200/50 dark:border-slate-700/50 py-3 z-50 transition-all duration-500 ease-out"
              >
                <div class="px-4 py-3 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 border-b border-gray-100 dark:border-slate-700">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-gray-900 dark:text-white">Результаты поиска</p>
                    <span class="text-xs text-gray-500 dark:text-gray-400">{{ searchResults.length }} найдено</span>
                  </div>
                </div>
                <div class="max-h-48 overflow-y-auto">
                  <div v-if="isSearching" class="px-6 py-8 text-center">
                    <div class="text-gray-500 dark:text-gray-400">
                      <div class="inline-flex items-center gap-3 mb-3">
                        <div class="w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                        <span class="font-medium text-gray-700 dark:text-gray-300">Идет поиск...</span>
                      </div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Находим лучшие товары для вас</p>
                    </div>
                  </div>
                  <div 
                    v-else-if="showSearchResults" 
                    v-for="(product, index) in searchResults" 
                    :key="product.id" 
                    @click="selectSearchResult(product)"
                    class="px-4 py-3 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 transition-all duration-300 cursor-pointer border-b border-gray-100 dark:border-slate-700 last:border-b-0 transform hover:scale-[1.02] hover:translate-x-1"
                    :style="{ animationDelay: `${index * 100}ms` }"
                  >
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-800 dark:to-pink-800 rounded-lg flex items-center justify-center flex-shrink-0 shadow-sm">
                        <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 dark:text-white truncate group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">{{ product.title }}</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">{{ product.price }} ₽</p>
                      </div>
                      <div class="w-5 h-5 text-gray-400 group-hover:text-purple-500 transition-colors flex-shrink-0">
                        <svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="searchQuery.length >= 2" class="px-6 py-8 text-center">
                    <div class="text-gray-500 dark:text-gray-400">
                      <div class="text-5xl mb-4 animate-bounce">🔍</div>
                      <p class="font-medium mb-2 text-gray-700 dark:text-gray-300">Ничего не найдено</p>
                      <p class="text-sm">Попробуйте изменить запрос</p>
                    </div>
                  </div>
                  <div v-else class="px-6 py-8 text-center">
                    <div class="text-gray-500 dark:text-gray-400">
                      <div class="text-4xl mb-3 text-purple-500 dark:text-purple-400">💡</div>
                      <p class="font-medium mb-2 text-gray-700 dark:text-gray-300">Введите минимум 2 символа для поиска</p>
                      <p class="text-sm">Начните печатать, чтобы найти товары</p>
                    </div>
                  </div>
                </div>
                <div v-if="searchQuery.trim() && !isSearching" class="px-4 py-3 border-t border-gray-100 dark:border-slate-700 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20">
                  <button 
                    @click="handleSearch"
                    class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    🔍 Показать все результаты для "{{ searchQuery }}"
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </transition>

      <!-- Mobile Navigation Menu -->
      <transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 -translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-4"
      >
        <div
          v-if="isMobileMenuOpen"
          class="md:hidden pb-4"
          data-mobile-menu
        >
          <div class="space-y-2">
            <!-- Кнопка профиля для аутентифицированных пользователей -->
            <router-link
              v-if="isAuthenticated"
              :to="user?.role === 'seller' ? '/seller' : '/buyer'"
              class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 rounded-xl transition-all duration-300"
              @click="closeMobileMenu"
            >
              <svg class="w-5 h-5 mr-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              {{ user?.role === 'seller' ? 'Мои товары' : 'Мои заказы' }}
            </router-link>
            
            <router-link
              to="/popular"
              class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 rounded-xl transition-all duration-300"
              @click="closeMobileMenu"
            >
              <svg class="w-5 h-5 mr-3 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
              Каталог
            </router-link>
            <router-link
              to="/blog"
              class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 rounded-xl transition-all duration-300"
              @click="closeMobileMenu"
            >
              <svg class="w-5 h-5 mr-3 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
              </svg>
              Блог
            </router-link>
            <router-link
              to="/support"
              class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 rounded-xl transition-all duration-300"
              @click="closeMobileMenu"
            >
              <svg class="w-5 h-5 mr-3 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 0l3.536 3.536m0 5.656l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              Поддержка
            </router-link>
          </div>
        </div>
      </transition>
  </nav>

  <!-- Spacer for fixed navbar -->
  <div class="h-16"></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuth } from '../composables/useAuth';
import { useRouter } from 'vue-router';
import { api } from '../api';

const router = useRouter();
const { isAuthenticated, user, logout: authLogout } = useAuth();

const isUserMenuOpen = ref(false);
const isMobileMenuOpen = ref(false);
const isSearchOpen = ref(false);
const searchQuery = ref('');
const isSearchFocused = ref(false);
const isSearchHovered = ref(false);
const searchResults = ref<any[]>([]);
const isSearching = ref(false);
const showSearchResults = ref(false);

// Timeout handlers for smooth hover
let searchHoverTimeout: number | null = null;
let userMenuTimeout: number | null = null;
let searchDebounceTimeout: number | null = null;

const userInitial = computed(() => {
  if (user.value?.email) {
    return user.value.email.charAt(0).toUpperCase();
  }
  return 'U';
});

const toggleUserMenu = () => {
  if (userMenuTimeout) {
    clearTimeout(userMenuTimeout);
    userMenuTimeout = null;
  }
  isUserMenuOpen.value = !isUserMenuOpen.value;
};

const openUserMenu = () => {
  if (userMenuTimeout) {
    clearTimeout(userMenuTimeout);
    userMenuTimeout = null;
  }
  isUserMenuOpen.value = true;
};

const closeUserMenu = () => {
  userMenuTimeout = setTimeout(() => {
    isUserMenuOpen.value = false;
  }, 300); // 300ms delay before closing
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
  if (isMobileMenuOpen.value) {
    isSearchOpen.value = false;
  }
};

const toggleSearch = () => {
  isSearchOpen.value = !isSearchOpen.value;
  if (isSearchOpen.value) {
    isMobileMenuOpen.value = false;
  }
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const logout = () => {
  authLogout();
  isUserMenuOpen.value = false;
};

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/search?q=${encodeURIComponent(searchQuery.value.trim())}`);
    // Очищаем поиск и скрываем результаты
    searchQuery.value = '';
    showSearchResults.value = false;
    isSearchFocused.value = false;
  }
};

const performSearch = async (query: string) => {
  if (!query.trim() || query.length < 2) {
    searchResults.value = [];
    showSearchResults.value = false;
    return;
  }

  try {
    isSearching.value = true;
    
    // Экранируем специальные символы для поиска
    const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    
    const response = await api.get(`/products/`, {
      params: {
        search: escapedQuery,
        limit: 5
      }
    });
    
    searchResults.value = response.data.results || [];
    showSearchResults.value = searchResults.value.length > 0;
  } catch (error) {
    console.error('Ошибка поиска:', error);
    searchResults.value = [];
    showSearchResults.value = false;
  } finally {
    isSearching.value = false;
  }
};

const debouncedSearch = (query: string) => {
  if (searchDebounceTimeout) {
    clearTimeout(searchDebounceTimeout);
  }
  
  searchDebounceTimeout = setTimeout(() => {
    performSearch(query);
  }, 300); // 300ms debounce
};

const handleSearchInput = () => {
  if (searchQuery.value && searchQuery.value.trim()) {
    debouncedSearch(searchQuery.value);
  } else {
    searchResults.value = [];
    showSearchResults.value = false;
  }
};

const selectSearchResult = (product: any) => {
  router.push(`/product/${product.id}`);
  // Очищаем поиск и скрываем результаты
  searchQuery.value = '';
  searchResults.value = [];
  showSearchResults.value = false;
  isSearchFocused.value = false;
};

const clearSearch = () => {
  searchQuery.value = '';
  searchResults.value = [];
  showSearchResults.value = false;
  isSearchFocused.value = false;
};

// Функции для анимации поля поиска
const getPlaceholder = () => {
  if (searchQuery.value) return '';
  if (isSearchFocused.value) return 'Поиск товаров...';
  return 'Поиск';
};

const getInputClasses = () => {
  const baseClasses = 'px-4 py-2 pr-12 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded-full text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-sm font-medium transition-all duration-500 ease-out';
  
  if (searchQuery.value || isSearchFocused.value) {
    return `${baseClasses} w-full`;
  }
  
  return `${baseClasses} w-28`;
};

const getMobileInputClasses = () => {
  const baseClasses = 'px-4 py-2 pr-12 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded-full text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-sm font-medium transition-all duration-500 ease-out';
  
  if (searchQuery.value || isSearchFocused.value) {
    return `${baseClasses} w-full`;
  }
  
  return `${baseClasses} w-28`;
};

const openSearchHover = () => {
  if (searchHoverTimeout) {
    clearTimeout(searchHoverTimeout);
    searchHoverTimeout = null;
  }
  isSearchHovered.value = true;
};

const closeSearchHover = () => {
  searchHoverTimeout = setTimeout(() => {
    isSearchHovered.value = false;
  }, 200); // 200ms delay before closing search
};

const handleSearchKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    handleSearch();
  }
};

// Close menus when clicking outside
const closeMenus = () => {
  // Clear all timeouts
  if (userMenuTimeout) {
    clearTimeout(userMenuTimeout);
    userMenuTimeout = null;
  }
  if (searchHoverTimeout) {
    clearTimeout(searchHoverTimeout);
    searchHoverTimeout = null;
  }
  if (searchDebounceTimeout) {
    clearTimeout(searchDebounceTimeout);
    searchDebounceTimeout = null;
  }
  
  isUserMenuOpen.value = false;
  isMobileMenuOpen.value = false;
  isSearchOpen.value = false;
  isSearchHovered.value = false;
};

// Close menus on route change
const handleRouteChange = () => {
  closeMenus();
};

// Close menus when clicking outside
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement;
  
  // Check if click is outside user menu
  if (!target.closest('[data-user-menu]') && isUserMenuOpen.value) {
    closeUserMenu();
  }
  
  // Check if click is outside search
  if (!target.closest('[data-search]') && isSearchHovered.value) {
    closeSearchHover();
  }
  
  // Check if click is outside mobile menu
  if (!target.closest('[data-mobile-menu]') && isMobileMenuOpen.value) {
    closeMobileMenu();
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  // Подписываемся на изменения маршрута
  router.afterEach(handleRouteChange);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  
  // Clear all timeouts
  if (userMenuTimeout) {
    clearTimeout(userMenuTimeout);
  }
  if (searchHoverTimeout) {
    clearTimeout(searchHoverTimeout);
  }
  if (searchDebounceTimeout) {
    clearTimeout(searchDebounceTimeout);
  }
});
</script>

<style scoped>
/* Custom scrollbar for dropdown */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.8);
}

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
</style>
  