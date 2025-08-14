<template>
  <div>
    <textarea
      :value="modelValue"
      @input="updateValue"
      class="mt-1 block w-full p-3 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 resize-y"
      rows="6"
      placeholder="Введите текст в формате Markdown..."
    ></textarea>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue']);

const updateValue = (event: Event) => {
  emit('update:modelValue', (event.target as HTMLTextAreaElement).value);
};
</script>

<style>
/* Минимальные стили для textarea */
textarea:focus {
  outline: none;
}

textarea::placeholder {
  color: #9ca3af; /* Tailwind gray-400 */
}

.dark textarea::placeholder {
  color: #64748b; /* Tailwind slate-500 */
}
</style>