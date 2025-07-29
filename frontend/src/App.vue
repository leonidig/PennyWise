<script setup>
import Navbar from '@/components/NavbarComp.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const hideNavbarOn = ['/login', '/register']
</script>

<template>
  <div class="min-h-screen bg-red-50 text-red-900 font-sans">
    <Navbar v-if="!hideNavbarOn.includes(route.path)" />
    <main class="px-4 py-6 w-full">
      <router-view />
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  background-color: #FEF2F2;
  color: #7F1D1D;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background-color: #DC2626;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #7F1D1D;
}
</style>
