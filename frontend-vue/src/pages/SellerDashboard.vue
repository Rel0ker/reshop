<script setup lang="ts">
import { ref, watchEffect, reactive, watch } from "vue";
import { api } from "../api";
import { useAuth } from "../composables/useAuth";
import noImage from '../assets/no-image.png';
import MarkdownEditor from '../components/MarkdownEditor.vue';
import { addSampleProducts as addSampleProductsUtil } from '../utils/addSampleProducts';

interface ProductImage {
  id: string;
  image: string;
}

interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  quantity: number;
  usage_instructions: string;
  seller: {
    id: string;
  };
  images: ProductImage[];
}

interface OrderItem {
  id: string;
  product: Product;
  quantity: number;
}

interface Order {
  id: string;
  seller: string;
  buyer: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'paid' | 'cancelled';
  created_at: string;
  comment?: string; // Добавляем поле comment
}

const { user } = useAuth();

const products = ref<Product[]>([]);
const orders = ref<Order[]>([]);
const showOrderDetailsModal = ref(false);
const selectedOrder = ref<Order | null>(null);

const showEditProductModal = ref(false);
const editingProduct = ref<Product | null>(null);
const editForm = reactive({
  id: '',
  title: '',
  description: '',
  price: 0,
  quantity: 0,
  usage_instructions: '',
  uploaded_images: [] as File[],
  existing_images: [] as ProductImage[],
});

const editImagePreviews = ref<string[]>([]); // URL для предварительного просмотра в форме редактирования

function openEditProductModal(product: Product) {
  editingProduct.value = product;
  editForm.id = product.id;
  editForm.title = product.title;
  editForm.description = product.description;
  editForm.price = product.price;
  editForm.quantity = product.quantity;
  editForm.usage_instructions = product.usage_instructions;
  editForm.existing_images = product.images;
  editForm.uploaded_images = [];
  showEditProductModal.value = true;
}

function closeEditProductModal() {
  showEditProductModal.value = false;
  editingProduct.value = null;
  editForm.uploaded_images = [];
  editForm.existing_images = [];
  
  // Очищаем предварительный просмотр
  editImagePreviews.value.forEach(url => URL.revokeObjectURL(url));
  editImagePreviews.value = [];
}

const handleEditFileChange = (e: Event) => {
  const files = (e.target as HTMLInputElement).files;
  if (files) {
    console.log('📁 Edit: Files selected:', files);
    console.log('📊 Edit: Total files:', files.length);
    
    // Валидация файлов
    const validFiles: File[] = [];
    const errors: string[] = [];
    
    Array.from(files).forEach((file, index) => {
      console.log(`🔍 Edit: Validating file ${index + 1}:`, {
        name: file.name,
        type: file.type,
        size: file.size,
        lastModified: file.lastModified
      });
      
      // Проверяем тип файла
      if (!file.type.startsWith('image/')) {
        errors.push(`Файл "${file.name}" не является изображением`);
        console.warn(`⚠️ Edit: File ${file.name} is not an image: ${file.type}`);
        return;
      }
      
      // Проверяем размер файла (максимум 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        errors.push(`Файл "${file.name}" слишком большой (максимум 5MB)`);
        console.warn(`⚠️ Edit: File ${file.name} is too large: ${file.size} bytes`);
        return;
      }
      
      validFiles.push(file);
      console.log(`✅ Edit: File ${file.name} is valid`);
    });
    
    // Показываем ошибки, если есть
    if (errors.length > 0) {
      alert(`Ошибки валидации:\n${errors.join('\n')}`);
    }
    
    // Ограничиваем количество файлов до 5
    const maxFiles = 5;
    if (validFiles.length > maxFiles) {
      alert(`Максимум ${maxFiles} изображений. Первые ${maxFiles} файлов будут загружены.`);
      validFiles.splice(maxFiles);
    }
    
    editForm.uploaded_images = validFiles;
    console.log('✅ Edit: Valid files set:', editForm.uploaded_images);
    console.log('📊 Edit: Final images count:', editForm.uploaded_images.length);
    
    // Создаем предварительный просмотр для новых изображений
    createEditImagePreviews(validFiles);
  }
};
const form = reactive({
  title: "", 
  description: "", 
  price: "", 
  quantity: 1, 
  usage_instructions: "",
  uploaded_images: [] as File[]
});

const imagePreviews = ref<string[]>([]); // URL для предварительного просмотра

const activeTab = ref('products'); // 'products', 'add' или 'orders'
const isAddingSamples = ref(false);
const isAddingProduct = ref(false); // Состояние загрузки при добавлении товара
const isUpdatingProduct = ref(false); // Состояние загрузки при обновлении товара
const uploadProgress = ref(0); // Прогресс загрузки
const sampleMessage = ref('');
const sampleProgress = ref(0);
const totalSamples = 35;

const addSampleProducts = async () => {
  if (isAddingSamples.value) return;
  
  isAddingSamples.value = true;
  sampleProgress.value = 0;
  sampleMessage.value = 'Начинаю добавление образцов товаров...';
  
  try {
    // Создаем функцию обратного вызова для обновления прогресса
    const updateProgress = (current: number) => {
      sampleProgress.value = Math.round((current / totalSamples) * 100);
      sampleMessage.value = `Добавляю товар ${current}/${totalSamples}...`;
    };
    
    await addSampleProductsUtil(updateProgress);
    sampleMessage.value = '✅ Все 35 образцов товаров успешно добавлены!';
    sampleProgress.value = 100;
    
    // Обновляем список товаров
    await fetchMine();
    
    // Показываем сообщение 5 секунд
    setTimeout(() => {
      sampleMessage.value = '';
      sampleProgress.value = 0;
    }, 5000);
    
  } catch (error) {
    console.error('Ошибка при добавлении образцов:', error);
    sampleMessage.value = '❌ Произошла ошибка при добавлении образцов товаров';
    
    // Показываем сообщение об ошибке 5 секунд
    setTimeout(() => {
      sampleMessage.value = '';
      sampleProgress.value = 0;
    }, 5000);
  } finally {
    isAddingSamples.value = false;
  }
};

async function fetchOrders() {
  try {
    console.log('[Dashboard] Запрашиваю заказы для пользователя...');
    const { data } = await api.get("/orders/mine/");
    console.log('[Dashboard] Заказы успешно загружены:', data);
    orders.value = data;
  } catch (error) {
    console.error("Ошибка при загрузке заказов продавца:", error);
    orders.value = [];
  }
}

async function fetchMine() {
  try {
    console.log('[Dashboard] Запрашиваю товары для пользователя...');
    const { data } = await api.get("/products/mine/");
    console.log('[Dashboard] Товары успешно загружены:', data);
    console.log('[Dashboard] Количество товаров:', data.length);
    products.value = data;
  } catch (error) {
    console.error("Ошибка при загрузке товаров продавца:", error);
    products.value = [];
  }
}

watchEffect(() => {
  console.log('[Dashboard] watchEffect сработал. ID пользователя:', user.value?.id);
  if (user.value?.id) {
    fetchMine();
    fetchOrders();
  } else {
    // Очищаем товары, если пользователь разлогинился
    products.value = [];
    orders.value = [];
  }
});

// Очищаем предварительный просмотр при смене вкладки
watch(activeTab, (newTab) => {
  if (newTab !== 'add') {
    // Очищаем предварительный просмотр и форму при уходе с вкладки добавления
    imagePreviews.value.forEach(url => URL.revokeObjectURL(url));
    imagePreviews.value = [];
    form.uploaded_images = [];
    
    const fileInput = document.getElementById('uploaded_images') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }
});

const handleFileChange = (e: Event) => {
  const files = (e.target as HTMLInputElement).files;
  if (files) {
    console.log('📁 Files selected:', files);
    console.log('📊 Total files:', files.length);
    
    // Валидация файлов
    const validFiles: File[] = [];
    const errors: string[] = [];
    
    Array.from(files).forEach((file, index) => {
      console.log(`🔍 Validating file ${index + 1}:`, {
        name: file.name,
        type: file.type,
        size: file.size,
        lastModified: file.lastModified
      });
      
      // Проверяем тип файла
      if (!file.type.startsWith('image/')) {
        errors.push(`Файл "${file.name}" не является изображением`);
        console.warn(`⚠️ File ${file.name} is not an image: ${file.type}`);
        return;
      }
      
      // Проверяем размер файла (максимум 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        errors.push(`Файл "${file.name}" слишком большой (максимум 5MB)`);
        console.warn(`⚠️ File ${file.name} is too large: ${file.size} bytes`);
        return;
      }
      
      validFiles.push(file);
      console.log(`✅ File ${file.name} is valid`);
    });
    
    // Показываем ошибки, если есть
    if (errors.length > 0) {
      alert(`Ошибки валидации:\n${errors.join('\n')}`);
    }
    
    // Ограничиваем количество файлов до 5
    const maxFiles = 5;
    if (validFiles.length > maxFiles) {
      alert(`Максимум ${maxFiles} изображений. Первые ${maxFiles} файлов будут загружены.`);
      validFiles.splice(maxFiles);
    }
    
    form.uploaded_images = validFiles;
    console.log('✅ Valid files set:', form.uploaded_images);
    console.log('📊 Final images count:', form.uploaded_images.length);
    
    // Создаем предварительный просмотр
    createImagePreviews(validFiles);
  }
};

const createImagePreviews = (files: File[]) => {
  // Очищаем старые предварительные просмотры
  imagePreviews.value.forEach(url => URL.revokeObjectURL(url));
  imagePreviews.value = [];
  
  files.forEach(file => {
    const url = URL.createObjectURL(file);
    imagePreviews.value.push(url);
    console.log(`🖼️ Created preview for ${file.name}:`, url);
  });
};

const createEditImagePreviews = (files: File[]) => {
  // Очищаем старые предварительные просмотры
  editImagePreviews.value.forEach(url => URL.revokeObjectURL(url));
  editImagePreviews.value = [];
  
  files.forEach(file => {
    const url = URL.createObjectURL(file);
    editImagePreviews.value.push(url);
    console.log(`🖼️ Edit: Created preview for ${file.name}:`, url);
  });
};

const addProduct = async () => {
  try {
    console.log('🚀 Starting addProduct...');
    console.log('📋 Form data:', form);
    console.log('🖼️ Uploaded images:', form.uploaded_images);
    console.log('📊 Images count:', form.uploaded_images.length);
    
    // Проверяем, есть ли изображения
    if (form.uploaded_images.length === 0) {
      console.warn('⚠️ No images selected');
      alert('Пожалуйста, выберите хотя бы одно изображение для товара');
      return;
    }
    
    // Начинаем загрузку
    isAddingProduct.value = true;
    uploadProgress.value = 0;
    
    const fd = new FormData();
    fd.append('title', form.title);
    fd.append('description', form.description);
    fd.append('price', String(form.price));
    fd.append('quantity', String(form.quantity));
    fd.append('usage_instructions', form.usage_instructions);
    
    console.log('📝 FormData created, appending images...');
    
    // Добавляем изображения с логированием
    form.uploaded_images.forEach((file, index) => {
      console.log(`📎 Appending file ${index + 1}/${form.uploaded_images.length}:`, {
        name: file.name,
        type: file.type,
        size: file.size,
        lastModified: file.lastModified
      });
      fd.append(`uploaded_images`, file);
      uploadProgress.value = ((index + 1) / form.uploaded_images.length) * 50; // 50% за подготовку
    });
    
    console.log('📤 Sending request to API...');
    console.log('🌐 API endpoint: /products/');
    console.log('🔑 Headers:', { 'Content-Type': 'multipart/form-data' });
    
    // Симулируем прогресс загрузки
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 5;
      }
    }, 100);
    
    const response = await api.post("/products/", fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    clearInterval(progressInterval);
    uploadProgress.value = 100;
    
    console.log('✅ Product created successfully!');
    console.log('📦 Response data:', response.data);
    console.log('🆔 Product ID:', response.data.id);
    
    // Сброс формы
    Object.assign(form, { 
      title: "", 
      description: "", 
      price: "", 
      quantity: 1, 
      usage_instructions: "",
      uploaded_images: []
    });
    
    // Сброс input файла
    const fileInput = document.getElementById('uploaded_images') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
    
    // Очищаем предварительный просмотр
    imagePreviews.value.forEach(url => URL.revokeObjectURL(url));
    imagePreviews.value = [];
    
    // Обновляем список товаров
    await fetchMine();
    
    // Переходим на вкладку товаров
    activeTab.value = 'products';
    
    // Показываем уведомление об успехе
    alert('🎉 Товар успешно добавлен!');
    
  } catch (error: any) {
    console.error('❌ Error in addProduct:', error);
    console.error('📊 Error details:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers
    });
    
    let errorMessage = 'Произошла ошибка при добавлении товара. Пожалуйста, попробуйте еще раз.';
    
    if (error.response?.data?.error) {
      errorMessage = `Ошибка: ${error.response.data.error}`;
    } else if (error.response?.data) {
      const errors = Object.values(error.response.data);
      errorMessage = `Ошибки валидации:\n${errors.join('\n')}`;
    } else if (error.response?.status === 500) {
      errorMessage = 'Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.';
    } else if (error.response?.status === 400) {
      errorMessage = 'Неверные данные запроса. Проверьте введенную информацию.';
    } else if (error.response?.status === 401) {
      errorMessage = 'Ошибка аутентификации. Пожалуйста, войдите в систему заново.';
    } else if (error.response?.status === 403) {
      errorMessage = 'Доступ запрещен. У вас нет прав для добавления товаров.';
    }
    
    alert(errorMessage);
  } finally {
    // Завершаем загрузку
    isAddingProduct.value = false;
    setTimeout(() => {
      uploadProgress.value = 0;
    }, 1000);
  }
};

const deleteProduct = async (id: string) => {
  if (!confirm('Вы уверены, что хотите удалить этот товар?')) return;
  
  try {
    await api.delete(`/products/${id}/`);
    await fetchMine();
  } catch (error: any) {
    if (error.response?.data) {
      alert(Object.values(error.response.data).join('\n'));
    } else {
      alert("Произошла ошибка при удалении товара");
    }
  }
};

      const updateProduct = async () => {
        try {
          console.log('🔄 Starting updateProduct...');
          console.log('📋 Edit form data:', editForm);
          console.log('🖼️ Edit uploaded images:', editForm.uploaded_images);
          console.log('🖼️ Edit existing images:', editForm.existing_images);
          
          // Начинаем загрузку
          isUpdatingProduct.value = true;
          
          // Add a check for editingProduct.value to ensure it's not null before proceeding
          if (!editingProduct.value) {
            console.error("Ошибка: Товар для редактирования не выбран.");
            alert("Ошибка: Товар для редактирования не выбран.");
            return; // Exit the function if no product is selected
          }

          console.log('📦 Editing product:', editingProduct.value.id);

          const formData = new FormData();
          // Append scalar fields
          formData.append('title', editForm.title);
          formData.append('description', editForm.description);
          formData.append('price', String(editForm.price));
          formData.append('quantity', String(editForm.quantity));
          formData.append('usage_instructions', editForm.usage_instructions);

          console.log('📝 FormData created, appending images...');

          // Append new uploaded images
          editForm.uploaded_images.forEach((file, index) => {
            console.log(`📎 Edit: Appending file ${index + 1}:`, {
              name: file.name,
              type: file.type,
              size: file.size
            });
            formData.append('uploaded_images', file);
          });

          // Append IDs of existing images to retain
          console.log('🔄 Appending existing image IDs...');
          editForm.existing_images.forEach(img => {
            console.log(`🖼️ Edit: Keeping existing image:`, img.id, img.image);
            formData.append('existing_images', img.id);
          });

          // Append IDs of images to delete
          const imagesToDelete = editingProduct.value.images
            .filter(img => !editForm.existing_images.some(eImg => eImg.id === img.id))
            .map(img => img.id);
          
          console.log('🗑️ Images to delete:', imagesToDelete);
          imagesToDelete.forEach(id => {
            formData.append('images_to_delete', id);
          });

          console.log('📤 Edit: Sending PATCH request to API...');
          console.log('🌐 Edit: API endpoint:', `/products/${editingProduct.value.id}/`);
          
          const response = await api.patch(`/products/${editingProduct.value.id}/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          
          console.log('✅ Edit: Product updated successfully!');
          console.log('📦 Edit: Response data:', response.data);
          
          const updatedProduct = response.data;
          
          // Обновляем товар в списке
          const index = products.value.findIndex(p => p.id === updatedProduct.id);
          if (index !== -1) {
            products.value[index] = updatedProduct;
            console.log('🔄 Edit: Products list updated at index:', index);
          } else {
            console.warn('⚠️ Edit: Product not found in list, refreshing...');
            // Если товар не найден в списке, обновляем весь список
            await fetchMine();
          }
          
          closeEditProductModal();
          alert('🎉 Товар успешно обновлен!');
          
          // Обновляем список товаров для отображения актуальных данных
          console.log('🔄 Edit: Refreshing products list...');
          await fetchMine();
          
        } catch (error: any) {
          console.error('❌ Edit: Error updating product:', error);
          console.error('📊 Edit: Error details:', {
            message: error.message,
            status: error.response?.status,
            statusText: error.response?.statusText,
            data: error.response?.data,
            headers: error.response?.headers
          });
          
          let errorMessage = 'Произошла ошибка при обновлении товара. Пожалуйста, попробуйте еще раз.';
          
          if (error.response?.data?.error) {
            errorMessage = `Ошибка: ${error.response.data.error}`;
          } else if (error.response?.data) {
            const errors = Object.values(error.response.data);
            errorMessage = `Ошибки валидации:\n${errors.join('\n')}`;
          } else if (error.response?.status === 500) {
            errorMessage = 'Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.';
          } else if (error.response?.status === 400) {
            errorMessage = 'Неверные данные запроса. Проверьте введенную информацию.';
          } else if (error.response?.status === 401) {
            errorMessage = 'Ошибка аутентификации. Пожалуйста, войдите в систему заново.';
          } else if (error.response?.status === 403) {
            errorMessage = 'Доступ запрещен. У вас нет прав для редактирования товаров.';
          }
          
          alert(errorMessage);
        } finally {
          // Завершаем загрузку
          isUpdatingProduct.value = false;
        }
      };

</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-pink-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-purple-600/20 via-pink-600/20 to-rose-600/20"></div>
      <div class="relative container mx-auto px-4 py-16">
        <div class="text-center">
          <h1 class="text-5xl md:text-6xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 bg-clip-text text-transparent mb-6">
            Панель продавца
          </h1>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Управляйте своими товарами, отслеживайте заказы и развивайте свой бизнес
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
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Всего товаров</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ products.length }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
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
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Общая выручка</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ orders.reduce((sum, order) => sum + order.total, 0) }} ₽</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg mb-8">
        <div class="flex flex-col sm:flex-row gap-4">
          <button 
            @click="activeTab = 'products'"
            :class="[
              'px-6 py-3 rounded-xl font-medium transition-all duration-300 transform hover:scale-105',
              activeTab === 'products' 
                ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg' 
                : 'bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-slate-600'
            ]"
          >
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
              Мои товары ({{ products.length }})
            </span>
          </button>
          
          <button 
            @click="activeTab = 'add'"
            :class="[
              'px-6 py-3 rounded-xl font-medium transition-all duration-300 transform hover:scale-105',
              activeTab === 'add' 
                ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-lg' 
                : 'bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-slate-600'
            ]"
          >
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Добавить товар
            </span>
          </button>
          
          <button 
            @click="activeTab = 'orders'"
            :class="[
              'px-6 py-3 rounded-xl font-medium transition-all duration-300 transform hover:scale-105',
              activeTab === 'orders' 
                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg' 
                : 'bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-slate-600'
            ]"
          >
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              Мои заказы ({{ orders.length }})
            </span>
          </button>
          
          <button 
            @click="addSampleProducts"
            :disabled="isAddingSamples"
            class="px-6 py-3 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            title="Добавить 35 образцов товаров"
          >
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <span v-if="isAddingSamples">⏳ Добавляю...</span>
              <span v-else>📦 Добавить образцы</span>
            </span>
          </button>
        </div>
      </div>

      <!-- Sample Messages -->
      <div v-if="sampleMessage" class="mb-8 p-6 rounded-2xl text-center border-2" :class="{
        'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200 border-green-200 dark:border-green-700': sampleMessage.includes('✅'),
        'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200 border-red-200 dark:border-red-700': sampleMessage.includes('❌'),
        'bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200 border-blue-200 dark:border-blue-700': !sampleMessage.includes('✅') && !sampleMessage.includes('❌')
      }">
        <div class="flex items-center justify-center space-x-2">
          <svg v-if="sampleMessage.includes('✅')" class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else-if="sampleMessage.includes('❌')" class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-lg font-medium">{{ sampleMessage }}</span>
        </div>
      </div>

      <!-- Вкладка "Мои товары" -->
      <div v-if="activeTab === 'products'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="product in products" :key="product.id" class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div class="relative">
            <img 
              :src="product.images[0]?.image || noImage" 
              :alt="`Product Image for ${product.title}`" 
              class="w-full aspect-square object-cover rounded-lg"
              @error="console.error('Image failed to load:', product.images[0]?.image)"
              @load="console.log('Image loaded successfully:', product.images[0]?.image)"
            />
            <div class="absolute top-3 right-3 flex space-x-2">
              <button @click="openEditProductModal(product)" class="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zm-3.586 3.586l-4.607 4.607a1 1 0 00-.279.487l-1.5 4.5a1 1 0 001.182 1.182l4.5-1.5a1 1 0 00.487-.279l4.607-4.607-2.828-2.828z" />
                </svg>
              </button>
              <button @click="deleteProduct(product.id)" class="bg-red-600 hover:bg-red-700 text-white p-2 rounded-full text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
          <div class="p-4">
            <h2 class="text-2xl font-bold mb-2">{{ product.title }}</h2>
            <p class="text-gray-600 dark:text-gray-300 text-sm mb-2">{{ product.description }}</p>
            <div class="flex justify-between items-center">
              <span class="text-2xl font-semibold text-gray-900 dark:text-white">{{ product.price }} ₽</span>
              <span class="text-gray-600 dark:text-gray-300">В наличии: {{ product.quantity }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Вкладка "Добавить товар" -->
      <div v-if="activeTab === 'add'" class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg">
        <h2 class="text-2xl font-bold mb-4">Добавить новый товар</h2>
        <form @submit.prevent="addProduct">
          <div class="mb-4">
            <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Название товара</label>
            <input type="text" id="title" v-model="form.title" class="mt-1 block w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white" required>
          </div>
          <div class="mb-4">
            <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Описание</label>
            <MarkdownEditor id="description" v-model="form.description" />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="price" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Цена</label>
              <input type="number" id="price" v-model="form.price" class="mt-1 block w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white" required>
            </div>
            <div>
              <label for="quantity" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Количество</label>
              <input type="number" id="quantity" v-model="form.quantity" class="mt-1 block w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white" required>
            </div>
          </div>
          <div class="mb-4">
            <label for="usage_instructions" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Инструкции по использованию</label>
            <MarkdownEditor id="usage_instructions" v-model="form.usage_instructions" />
           </div>
           <div class="mb-4">
            <label for="uploaded_images" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Изображения <span class="text-red-400">*</span> (до 5, обязательно)
            </label>
            <input type="file" id="uploaded_images" @change="handleFileChange" multiple accept="image/*" class="mt-1 block w-full text-sm text-gray-700 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100 dark:file:bg-purple-900 dark:file:text-purple-300" required>
            
            <!-- Предварительный просмотр изображений -->
            <div v-if="imagePreviews.length > 0" class="mt-4">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Предварительный просмотр:</h4>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                <div v-for="(preview, index) in imagePreviews" :key="index" class="relative group">
                  <img :src="preview" :alt="`Preview ${index + 1}`" class="w-full aspect-square object-cover rounded-lg border-2 border-gray-300 dark:border-slate-600 group-hover:border-purple-500 transition-colors dark:bg-slate-700"/>
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all rounded-lg flex items-center justify-center">
                    <span class="text-white text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity">
                      {{ form.uploaded_images[index]?.name || `Image ${index + 1}` }}
                    </span>
                  </div>
                </div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-400 mt-2">
                Выбрано изображений: {{ imagePreviews.length }}/5
              </p>
            </div>
          </div>
          
          <!-- Прогресс-бар загрузки -->
          <div v-if="isAddingProduct" class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Загрузка товара...</span>
              <span class="text-sm text-gray-600 dark:text-gray-400">{{ Math.round(uploadProgress) }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
              <div 
                class="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-300 ease-out"
                :style="{ width: uploadProgress + '%' }"
              ></div>
            </div>
          </div>
          
          <button 
            type="submit" 
            :disabled="isAddingProduct || form.uploaded_images.length === 0"
            class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isAddingProduct" class="flex items-center gap-2">
              <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Загружаю...
            </span>
            <span v-else class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Добавить товар
            </span>
          </button>
        </form>
      </div>

      <!-- Вкладка "Мои заказы" -->
      <div v-if="activeTab === 'orders'" class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg">
        <h2 class="text-2xl font-bold mb-4">Мои заказы</h2>
        <div v-if="orders.length === 0" class="text-gray-600 dark:text-gray-300">У вас пока нет заказов.</div>
        <div v-else>
          <div v-for="order in orders" :key="order.id" class="bg-gray-100 dark:bg-slate-700 p-4 rounded-lg mb-4 shadow-sm">
            <h3 class="text-2xl font-bold mb-2">Заказ #{{ order.id.substring(0, 8) }}</h3>
            <p class="text-gray-600 dark:text-gray-300">Покупатель: {{ order.buyer }}</p>
            <p class="text-gray-600 dark:text-gray-300">Статус: {{ order.status }}</p>
            <p class="text-gray-600 dark:text-gray-300">Дата: {{ new Date(order.created_at).toLocaleDateString() }}</p>
            <p class="text-gray-600 dark:text-gray-300">Общая сумма: {{ order.total }} ₽</p>
            <div class="mt-4">
              <h4 class="font-semibold mb-2">Товары:</h4>
              <div v-for="item in order.items" :key="item.product.id" class="flex items-center mb-2">
                <img :src="item.product.images[0]?.image || noImage" alt="Product Image" class="w-20 h-20 object-cover rounded-md mr-4" />
                <div>
                  <p class="font-medium">{{ item.product.title }}</p>
                  <p class="text-gray-600 dark:text-gray-300 text-sm">Количество: {{ item.quantity }}</p>
                </div>
              </div>
            </div>
            <div v-if="order.comment" class="mt-4 p-3 bg-gray-200 dark:bg-slate-600 rounded-lg text-gray-800 dark:text-gray-200">
              <h4 class="font-semibold mb-2">Комментарий к заказу:</h4>
              <p>{{ order.comment }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Модальное окно редактирования товара -->
      <div v-if="showEditProductModal" class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50">
        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg">
          <button @click="closeEditProductModal" class="absolute top-3 right-3 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white text-2xl font-semibold">&times;</button>
          <h2 class="text-2xl font-bold mb-4">Редактировать товар</h2>
          
          <form @submit.prevent="updateProduct">
            <div class="mb-4">
              <label for="edit-title" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Название товара</label>
              <input type="text" id="edit-title" v-model="editForm.title" class="mt-1 block w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white" required>
            </div>
            <div class="mb-4">
              <label for="edit-description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Описание</label>
              <MarkdownEditor id="edit-description" v-model="editForm.description" />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label for="edit-price" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Цена в ₽</label>
                <input type="number" id="edit-price" v-model="editForm.price" class="mt-1 block w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white" required>
              </div>
              <div>
                <label for="edit-quantity" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Количество</label>
                <input type="number" id="edit-quantity" v-model="editForm.quantity" class="mt-1 block w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white" required>
              </div>
            </div>
            <div class="mb-4">
              <label for="edit-usage_instructions" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Инструкции по использованию</label>
              <MarkdownEditor id="edit-usage_instructions" v-model="editForm.usage_instructions" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Существующие изображения</label>
              <div class="flex flex-wrap gap-2 mt-2">
                <div v-for="image in editForm.existing_images" :key="image.id" class="relative w-20 h-20">
                  <img :src="image.image" alt="Product Image" class="w-full h-full object-cover rounded-lg"/>
                  <button @click="editForm.existing_images = editForm.existing_images.filter(img => img.id !== image.id)" type="button" class="absolute top-0 right-0 bg-red-600 rounded-full p-1 text-white text-xs">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div class="mb-4">
              <label for="edit-uploaded_images" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Добавить новые изображения (до 5)</label>
              <input type="file" id="edit-uploaded_images" @change="handleEditFileChange" multiple accept="image/*" class="mt-1 block w-full text-sm text-gray-700 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100 dark:file:bg-purple-900 dark:file:text-purple-300">
              
              <!-- Предварительный просмотр новых изображений -->
              <div v-if="editImagePreviews.length > 0" class="mt-4">
                <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Предварительный просмотр новых изображений:</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                  <div v-for="(preview, index) in editImagePreviews" :key="index" class="relative group">
                    <img :src="preview" :alt="`New Preview ${index + 1}`" class="w-full aspect-square object-cover rounded-lg border-2 border-purple-500 group-hover:border-purple-400 transition-colors dark:bg-slate-700"/>
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all rounded-lg flex items-center justify-center">
                      <span class="text-white text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity">
                        {{ editForm.uploaded_images[index]?.name || `New Image ${index + 1}` }}
                      </span>
                    </div>
                  </div>
                </div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mt-2">
                  Новых изображений: {{ editImagePreviews.length }}/5
                </p>
              </div>
            </div>
            <button 
              type="submit" 
              :disabled="isUpdatingProduct"
              class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isUpdatingProduct" class="flex items-center gap-2">
                <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Обновляю...
              </span>
              <span v-else class="flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Сохранить изменения
              </span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
