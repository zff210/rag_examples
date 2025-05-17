<script setup>
import { ref } from 'vue';
import Sidebar from './components/Sidebar.vue';
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <router-view></router-view>
  </div>
</template>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply antialiased;
}
</style>
