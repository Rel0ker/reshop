<script setup lang="ts">
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter();

onMounted(() => {
  router.replace('/register/buyer');
});
</script>

<template>
  <div>
    <!-- Перенаправление на страницу регистрации покупателя... -->
  </div>
</template>
