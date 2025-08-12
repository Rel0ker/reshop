<script setup lang="ts">
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";
</script>

<template class="bg-black">
  <div class="min-h-screen flex flex-col bg-black">
    <Navbar class="fixed top-0 left-0 w-full z-50" />
    <main class="flex-grow">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;
</style>



