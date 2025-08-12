<template>
  <div class="relative group z-10">
    <div 
      @click="toggleDropdown"
      @mouseenter="onMouseEnter"
      @mouseleave="onMouseLeave"
      @keydown.enter="toggleDropdown"
      @keydown.space="toggleDropdown"
      @keydown.escape="isOpen = false"
      tabindex="0"
      role="button"
      aria-haspopup="true"
      :aria-expanded="isOpen"
      class="flex items-center gap-3 px-6 py-4 bg-white/80 dark:bg-white/10 backdrop-blur-md border border-gray-200 dark:border-white/20 rounded-2xl cursor-pointer hover:bg-white/90 dark:hover:bg-white/20 transition-all duration-300 group-hover:border-purple-500/50 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
    >
      <svg class="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
      </svg>
      <span class="text-gray-700 dark:text-gray-200 font-medium" :aria-label="`${label || 'Сортировка'}: ${currentOptionName}`">{{ label || 'Сортировка' }}</span>
      <svg class="w-4 h-4 text-gray-500 dark:text-gray-400 transition-transform duration-200" :class="{ 'rotate-180': isOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
    
    <!-- Dropdown Menu using Teleport -->
    <Teleport to="body">
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 scale-95 translate-y-2"
        enter-to-class="opacity-100 scale-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 scale-100 translate-y-0"
        leave-to-class="opacity-0 scale-95 translate-y-2"
      >
        <div 
          v-if="isOpen"
          @mouseenter="onMouseEnter"
          @mouseleave="onMouseLeave"
          role="listbox"
          :aria-label="`${label || 'Сортировка'}: выберите опцию`"
          :style="dropdownPosition"
          class="fixed bg-white/95 dark:bg-slate-800/95 backdrop-blur-md border border-gray-200 dark:border-slate-700 rounded-2xl shadow-2xl shadow-purple-500/20 z-50 max-h-96 overflow-y-auto w-80"
        >
          <div class="p-2">
            <div
              v-for="option in options"
              :key="option.id"
              @click="selectOption(option.id)"
              @keydown.enter="selectOption(option.id)"
              @keydown.space="selectOption(option.id)"
              tabindex="0"
              role="option"
              :aria-selected="modelValue === option.id"
              :class="[
                'flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer transition-all duration-200 hover:bg-purple-50 dark:hover:bg-purple-900/20 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-1',
                modelValue === option.id
                  ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-slate-700'
                  : 'text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
              ]"
            >
              <span class="text-lg flex-shrink-0">{{ option.icon }}</span>
              <span class="font-medium flex-1 min-w-0">{{ option.name }}</span>
              <div v-if="modelValue === option.id" class="ml-auto flex-shrink-0">
                <svg class="w-4 h-4 text-purple-600 dark:text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';

interface SortOption {
  id: string;
  name: string;
  icon: string;
}

interface Props {
  modelValue: string;
  options: SortOption[];
  label?: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'update:modelValue': [value: string];
}>();

const isOpen = ref(false);
const dropdownPosition = ref({ top: '0px', left: '0px' });
let hoverTimeout: number | null = null;
let buttonElement: HTMLElement | null = null;

const currentOptionName = computed(() => {
  const currentOption = props.options.find(option => option.id === props.modelValue);
  return currentOption ? currentOption.name : 'Не выбрано';
});

const updateDropdownPosition = async () => {
  if (!buttonElement) return;
  
  await nextTick();
  const rect = buttonElement.getBoundingClientRect();
  const top = rect.bottom + window.scrollY + 8; // 8px отступ
  const left = rect.left + window.scrollX;
  
  dropdownPosition.value = {
    top: `${top}px`,
    left: `${left}px`
  };
};

const toggleDropdown = async () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    await updateDropdownPosition();
  }
};

const selectOption = (optionId: string) => {
  emit('update:modelValue', optionId);
  isOpen.value = false;
};

const onMouseEnter = async () => {
  if (hoverTimeout) {
    clearTimeout(hoverTimeout);
    hoverTimeout = null;
  }
  isOpen.value = true;
  await updateDropdownPosition();
};

const onMouseLeave = () => {
  hoverTimeout = setTimeout(() => {
    isOpen.value = false;
  }, 300); // 300ms delay before closing
};

// Закрыть dropdown при клике вне его
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement;
  if (!target.closest('.relative')) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('resize', updateDropdownPosition);
  window.addEventListener('scroll', updateDropdownPosition);
  buttonElement = document.querySelector('[role="button"]') as HTMLElement;
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('resize', updateDropdownPosition);
  window.removeEventListener('scroll', updateDropdownPosition);
  if (hoverTimeout) {
    clearTimeout(hoverTimeout);
  }
});
</script>

<style scoped>
/* Ensure text doesn't get cut off */
.font-medium {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Custom scrollbar for dropdown */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.8);
}
</style>
