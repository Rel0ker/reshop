<script setup lang="ts">
import { ref, watchEffect, reactive, watch, computed } from "vue";
import { api } from "../api";
import { useAuth } from "../composables/useAuth";
import noImage from '../assets/no-image.png';
import MarkdownEditor from '../components/MarkdownEditor.vue';
import { addSampleProducts as addSampleProductsUtil } from '../utils/addSampleProducts';
import { marked } from 'marked';
import ProductCardNew from '@/components/ProductCardNew.vue';
import SellerProductCard from '@/components/SellerProductCard.vue';

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
  product: Product;
  quantity: number;
  total_amount: number;
  status: 'pending' | 'paid' | 'delivered' | 'payment_rejected' | 'seller_rejected' | 'canceled';
  created_at: string;
  comment?: string;
  receipt_email?: string;
  buyer: {
    id: string;
    email: string;
    username: string;
  };
}

const { user } = useAuth();

const products = ref<Product[]>([]);
const orders = ref<Order[]>([]);
const showOrderDetailsModal = ref(false);
const selectedOrder = ref<Order | null>(null);

// Фильтрация заказов
const selectedStatus = ref<string>('all');
const filteredOrders = computed(() => {
  if (selectedStatus.value === 'all') {
    return orders.value;
  }
  return orders.value.filter(order => order.status === selectedStatus.value);
});

// Computed свойство для превью товара в редакторе
const previewProduct = computed(() => ({
  id: editForm.id || 'preview',
  title: editForm.title || 'Название товара',
  description: editForm.description || 'Описание товара не заполнено',
  price: String(editForm.price || 0),
  quantity: editForm.quantity || 0,
  seller: { id: '', email: '' },
  images: editForm.existing_images.map(img => ({
    id: img.id,
    image: img.image,
    product: img.id
  })),
  image_url: editForm.existing_images.length > 0 ? editForm.existing_images[0].image : undefined
}));

// Функции для рендеринга Markdown в предварительном просмотре
const renderMarkdown = (text: string) => {
  return marked(text || '', { gfm: true });
};

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

// Функция для получения текста статуса заказа
function getStatusText(status: string): string {
  const statusMap: Record<string, string> = {
    'pending': 'В ожидании оплаты',
    'paid': 'Оплачен',
    'delivered': 'Завершен',
    'payment_rejected': 'Отклонен платежной системой',
    'seller_rejected': 'Отклонен продавцом',
    'canceled': 'Отменен'
  };
  return statusMap[status] || status;
}

// Функции для взаимодействия с заказами
async function confirmOrder(orderId: string) {
  try {
    const response = await api.post(`/orders/${orderId}/confirm/`);
    console.log('Заказ подтвержден:', response.data);
    
    // Обновляем статус заказа в локальном состоянии
    const orderIndex = orders.value.findIndex(o => o.id === orderId);
    if (orderIndex !== -1) {
      orders.value[orderIndex].status = 'paid';
    }
    
    // Показываем уведомление об успехе
    alert('Заказ успешно подтвержден!');
  } catch (error) {
    console.error('Ошибка при подтверждении заказа:', error);
    alert('Ошибка при подтверждении заказа');
  }
}

async function rejectOrder(orderId: string) {
  try {
    const response = await api.post(`/orders/${orderId}/reject/`);
    console.log('Заказ отклонен:', response.data);
    
    // Обновляем статус заказа в локальном состоянии
    const orderIndex = orders.value.findIndex(o => o.id === orderId);
    if (orderIndex !== -1) {
      orders.value[orderIndex].status = 'seller_rejected';
    }
    
    // Показываем уведомление об успехе
    alert('Заказ отклонен!');
  } catch (error) {
    console.error('Ошибка при отклонении заказа:', error);
    alert('Ошибка при отклонении заказа');
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
      
      <!-- Дополнительная статистика -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Общая выручка</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ orders.reduce((sum, order) => sum + (order.total_amount || 0), 0).toFixed(2) }} ₽</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-r from-yellow-500 to-orange-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
            </div>
          </div>
        </div>
        
        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Отклоненные заказы</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ orders.filter(o => o.status === 'payment_rejected' || o.status === 'seller_rejected').length }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-r from-red-500 to-pink-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
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
      <div v-if="activeTab === 'products'">
        <!-- Список товаров -->
        <div v-if="products.length > 0">
          <!-- Группировка товаров -->
          <div class="mb-6">
            <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">
              Товары в наличии ({{ products.filter(p => p.quantity > 0).length }})
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <SellerProductCard
                v-for="product in products.filter(p => p.quantity > 0)"
                :key="product.id"
                :product="product"
                @edit="openEditProductModal"
                @delete="deleteProduct"
              />
            </div>
          </div>
          
          <!-- Товары не в наличии -->
          <div v-if="products.filter(p => p.quantity <= 0).length > 0" class="mt-8">
            <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">
              Товары не в наличии ({{ products.filter(p => p.quantity <= 0).length }})
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <SellerProductCard
                v-for="product in products.filter(p => p.quantity <= 0)"
                :key="product.id"
                :product="product"
                @edit="openEditProductModal"
                @delete="deleteProduct"
              />
            </div>
          </div>
        </div>
        
        <!-- Сообщение об отсутствии товаров -->
        <div v-else class="text-center py-16">
          <div class="max-w-md mx-auto">
            <div class="text-6xl mb-4">📦</div>
            <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
              У вас пока нет товаров
            </h3>
            <p class="text-gray-500 dark:text-gray-400 mb-6">
              Создайте свой первый цифровой товар и начните зарабатывать
            </p>
            <button
              @click="activeTab = 'add'"
              class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105"
            >
              Создать товар
            </button>
          </div>
        </div>
      </div>

      <!-- Вкладка "Добавить товар" -->
      <div v-if="activeTab === 'add'" class="bg-white/80 dark:bg-slate-800/80 backdrop-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg">
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
      <div v-if="activeTab === 'orders'" class="bg-white/80 dark:bg-slate-800/80 backdrop-sm rounded-2xl p-6 border border-gray-200/50 dark:border-slate-700/50 shadow-lg">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-white">Мои заказы</h2>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Всего заказов: {{ orders.length }}
          </div>
        </div>
        
        <!-- Фильтр по статусам -->
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Фильтр по статусу:</h3>
          <div class="flex flex-wrap gap-2">
            <button
              @click="selectedStatus = 'all'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
                selectedStatus === 'all'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600'
              ]"
            >
              Все заказы ({{ orders.length }})
            </button>
            <button
              @click="selectedStatus = 'pending'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
                selectedStatus === 'pending'
                  ? 'bg-yellow-600 text-white shadow-lg'
                  : 'bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600'
              ]"
            >
              В ожидании оплаты ({{ orders.filter(o => o.status === 'pending').length }})
            </button>
            <button
              @click="selectedStatus = 'paid'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
                selectedStatus === 'paid'
                  ? 'bg-green-600 text-white shadow-lg'
                  : 'bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600'
              ]"
            >
              Оплачен ({{ orders.filter(o => o.status === 'paid').length }})
            </button>
            <button
              @click="selectedStatus = 'delivered'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
                selectedStatus === 'delivered'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600'
              ]"
            >
              Завершен ({{ orders.filter(o => o.status === 'delivered').length }})
            </button>
            <button
              @click="selectedStatus = 'payment_rejected'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
                selectedStatus === 'payment_rejected'
                  ? 'bg-red-600 text-white shadow-lg'
                  : 'bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600'
              ]"
            >
              Отклонен платежной системой ({{ orders.filter(o => o.status === 'payment_rejected').length }})
            </button>
            <button
              @click="selectedStatus = 'seller_rejected'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
                selectedStatus === 'seller_rejected'
                  ? 'bg-orange-600 text-white shadow-lg'
                  : 'bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600'
              ]"
            >
              Отклонен продавцом ({{ orders.filter(o => o.status === 'seller_rejected').length }})
            </button>
            <button
              @click="selectedStatus = 'canceled'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
                selectedStatus === 'canceled'
                  ? 'bg-gray-600 text-white shadow-lg'
                  : 'bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600'
              ]"
            >
              Отменен ({{ orders.filter(o => o.status === 'canceled').length }})
            </button>
          </div>
        </div>
        
        <div v-if="filteredOrders.length === 0" class="text-center py-12">
          <div class="w-24 h-24 mx-auto mb-4 bg-gray-200 dark:bg-slate-700 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-400 dark:text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {{ selectedStatus === 'all' ? 'Заказов пока нет' : `Заказов со статусом "${getStatusText(selectedStatus)}" не найдено` }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            {{ selectedStatus === 'all' ? 'Когда покупатели будут заказывать ваши товары, они появятся здесь' : 'Попробуйте изменить фильтр или дождитесь новых заказов' }}
          </p>
        </div>
        
        <div v-else>
          <div v-for="order in filteredOrders" :key="order.id" class="bg-gray-100 dark:bg-slate-700 p-4 rounded-lg mb-4 shadow-sm text-white">
            <h3 class="text-2xl font-bold mb-2">Заказ #{{ order.id.substring(0, 8) }}</h3>
            <p class="text-gray-600 dark:text-gray-300">Покупатель: {{ order.buyer?.email || 'Неизвестно' }}</p>
            <p class="text-gray-600 dark:text-gray-300">Статус: {{ order.status }}</p>
            <p class="text-gray-600 dark:text-gray-300">Дата: {{ new Date(order.created_at).toLocaleDateString() }}</p>
            <p class="text-gray-600 dark:text-gray-300">Общая сумма: {{ order.total_amount }} ₽</p>
            <div class="mt-4">
              <h4 class="font-semibold mb-2">Товар:</h4>
              <div class="flex items-center mb-2">
                <img :src="order.product?.images?.[0]?.image || noImage" alt="Product Image" class="w-20 h-20 object-cover rounded-md mr-4" />
                <div>
                  <p class="font-medium">{{ order.product?.title || 'Товар без названия' }}</p>
                  <p class="text-gray-600 dark:text-gray-300 text-sm">Количество: {{ order.quantity }}</p>
                  <p class="text-gray-600 dark:text-gray-300 text-sm">Цена: {{ order.product?.price }} ₽</p>
                </div>
              </div>
            </div>
            <div v-if="order.comment" class="mt-4 p-3 bg-gray-200 dark:bg-slate-600 rounded-lg text-gray-800 dark:text-gray-200">
              <h4 class="font-semibold mb-2">Комментарий к заказу:</h4>
              <p>{{ order.comment }}</p>
            </div>
            
            <!-- Кнопки взаимодействия для продавца -->
            <div v-if="order.status === 'pending'" class="mt-4 flex gap-2">
              <button 
                @click="confirmOrder(order.id)"
                class="flex-1 py-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg font-medium hover:from-green-600 hover:to-emerald-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Подтвердить
              </button>
              <button 
                @click="rejectOrder(order.id)"
                class="flex-1 py-2 bg-gradient-to-r from-red-500 to-pink-600 text-white rounded-lg font-medium hover:from-red-600 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Отклонить
              </button>
            </div>
            
            <!-- Статус для других состояний -->
            <div v-else class="mt-4">
              <div class="text-center py-2 px-3 rounded-lg font-medium text-sm"
                   :class="{
                     'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300': order.status === 'paid',
                     'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300': order.status === 'delivered',
                     'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300': order.status === 'payment_rejected',
                     'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-300': order.status === 'seller_rejected',
                     'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300': order.status === 'canceled'
                   }">
                {{ getStatusText(order.status) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Модальное окно редактирования товара -->
      <div v-if="showEditProductModal" class="fixed inset-0 bg-gray-900 bg-opacity-95 flex z-50">
        <!-- Левая колонка - Форма редактирования -->
        <div class="w-1/2 bg-white dark:bg-slate-800 overflow-y-auto">
          <!-- Заголовок -->
          <div class="sticky top-0 bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-slate-700 p-7 h-[97px] shadow-sm">
            <div class="flex items-center justify-between">
              <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Редактор товара</h2>
              
            </div>
          </div>
          
          <!-- Форма редактирования -->
          <div class="p-8">
            <form @submit.prevent="updateProduct" class="space-y-8">
              <div>
                <label for="edit-title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Название товара</label>
                <input type="text" id="edit-title" v-model="editForm.title" class="w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300" required>
              </div>
              
              <div>
                <label for="edit-description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Описание</label>
                <div class="border border-gray-300 dark:border-slate-600 rounded-lg overflow-hidden">
                  <MarkdownEditor id="edit-description" v-model="editForm.description" />
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="edit-price" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Цена в ₽</label>
                  <input type="number" id="edit-price" v-model="editForm.price" class="w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300" required>
                </div>
                <div>
                  <label for="edit-quantity" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Количество</label>
                  <input type="number" id="edit-quantity" v-model="editForm.quantity" class="w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300" required>
                </div>
              </div>
              
              <div>
                <label for="edit-usage_instructions" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Инструкции по использованию</label>
                <div class="border border-gray-300 dark:border-slate-600 rounded-lg overflow-hidden">
                  <MarkdownEditor id="edit-usage_instructions" v-model="editForm.usage_instructions" />
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Существующие изображения</label>
                <div class="flex flex-wrap gap-3">
                  <div v-for="image in editForm.existing_images" :key="image.id" class="relative group">
                    <img :src="image.image" alt="Product Image" class="w-24 h-24 object-cover rounded-lg border-2 border-gray-300 dark:border-slate-600 group-hover:border-purple-500 transition-all duration-300"/>
                    <button 
                      @click="editForm.existing_images = editForm.existing_images.filter(img => img.id !== image.id)" 
                      type="button" 
                      class="absolute -top-2 -right-2 bg-red-600 hover:bg-red-700 rounded-full p-1.5 text-white text-xs shadow-lg transition-all duration-300 transform hover:scale-110"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
                <p v-if="editForm.existing_images.length === 0" class="text-sm text-gray-500 dark:text-gray-400 mt-2">Нет существующих изображений</p>
              </div>
              
              <div>
                <label for="edit-uploaded_images" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Добавить новые изображения (до 5)</label>
                <input type="file" id="edit-uploaded_images" @change="handleEditFileChange" multiple accept="image/*" class="w-full text-sm text-gray-700 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100 dark:file:bg-purple-900 dark:file:text-purple-300">
                
                <!-- Предварительный просмотр новых изображений -->
                <div v-if="editImagePreviews.length > 0" class="mt-4">
                  <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Предварительный просмотр новых изображений:</h4>
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
                class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:-translate-y-1"
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

        <!-- Правая колонка - Предварительный просмотр -->
        <div class="w-1/2 bg-gray-50 dark:bg-slate-900 overflow-y-auto">
          <!-- Заголовок предварительного просмотра -->
          <div class="sticky top-0 bg-gray-50 dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700 p-4 shadow-sm z-10">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Предварительный просмотр</h3>
                <p class="text-gray-600 dark:text-gray-400 mt-2">Как будет выглядеть товар после сохранения</p>
              </div>
            
            <button 
                @click="closeEditProductModal" 
                class="w-10 h-10 bg-gray-100 dark:bg-slate-700 rounded-full flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-slate-600 hover:text-gray-900 dark:hover:text-white transition-all duration-300"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
          </div></div>

          <!-- Содержимое предварительного просмотра -->
          <div class="p-8 space-y-8">
            <!-- Превью товара -->
            <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-slate-700 w-96">
              <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Карточка товара</h4>
              
                              
                <ProductCardNew 
                  :product="previewProduct" style="z-index: 1;"
                />
            </div>

            <!-- Превью описания -->
            <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-slate-700">
              <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Описание товара</h4>
              <div class="prose prose-sm max-w-none dark:prose-invert">
                <div v-if="editForm.description" v-html="renderMarkdown(editForm.description)" class="text-gray-700 dark:text-gray-300"></div>
                <div v-else class="text-gray-500 dark:text-gray-400 italic">Описание товара не заполнено</div>
              </div>
            </div>

            <!-- Превью инструкций -->
            <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-slate-700">
              <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Инструкции по использованию</h4>
              <div class="prose prose-sm max-w-none dark:prose-invert">
                <div v-if="editForm.usage_instructions" v-html="renderMarkdown(editForm.usage_instructions)" class="text-gray-700 dark:text-gray-300"></div>
                <div v-else class="text-gray-500 dark:text-gray-400 italic">Инструкции не заполнены</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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
