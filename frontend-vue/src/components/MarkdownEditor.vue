<template>
  <div>
    <textarea
      :value="modelValue"
      @input="updateValue"
      class="mt-1 block w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white"
      rows="5"
    ></textarea>
    <div
      v-html="renderedMarkdown"
      class="mt-2 p-2 bg-gray-800 border border-gray-600 rounded-md text-gray-200 prose prose-invert"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { marked } from 'marked';

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

const renderedMarkdown = computed(() => {
  return marked(props.modelValue);
});
</script>

<style>
/* Basic Prose styles for rendered markdown */
.prose {
  color: inherit;
}
.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
  color: inherit;
  font-weight: bold;
}
.prose p {
  margin-bottom: 1em;
}
.prose ul,
.prose ol {
  list-style-position: inside;
  margin-bottom: 1em;
  padding-left: 1.5em;
}
.prose li {
  margin-bottom: 0.5em;
}
.prose a {
  color: #9333ea; /* Tailwind purple-600 */
  text-decoration: underline;
}
.prose code {
  background-color: #4b5563; /* Tailwind gray-600 */
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  font-family: monospace;
}
.prose pre {
  background-color: #1f2937; /* Tailwind gray-800 */
  padding: 1em;
  border-radius: 0.5em;
  overflow-x: auto;
}
.prose blockquote {
  border-left: 4px solid #6b7280; /* Tailwind gray-500 */
  padding-left: 1em;
  margin-left: 0;
  font-style: italic;
}
.prose table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}
.prose th,
.prose td {
  border: 1px solid #4b5563; /* Tailwind gray-600 */
  padding: 0.5em;
  text-align: left;
}
.prose img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5em;
}

/* Invert colors for dark mode */
.prose-invert h1, .prose-invert h2, .prose-invert h3, .prose-invert h4, .prose-invert h5, .prose-invert h6 {
  color: inherit;
}
.prose-invert p {
  color: inherit;
}
.prose-invert a {
  color: #a78bfa; /* Tailwind purple-400 */
}
.prose-invert code {
  background-color: #374151; /* Tailwind gray-700 */
}
.prose-invert pre {
  background-color: #111827; /* Tailwind gray-900 */
}
.prose-invert blockquote {
  border-left-color: #9ca3af; /* Tailwind gray-400 */
}
.prose-invert th,
.prose-invert td {
  border-color: #374151; /* Tailwind gray-700 */
}
</style>