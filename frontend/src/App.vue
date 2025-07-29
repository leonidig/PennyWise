<script setup>
import Navbar from '@/components/NavbarComp.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const hideNavbarOn = ['/login', '/register']
</script>

<template>
  <div class="min-h-screen bg-red-50 text-red-900 font-sans">
    <Navbar v-if="!hideNavbarOn.includes(route.path)" />
    <main class="px-4 py-6 max-w-4xl mx-auto">
      <router-view />
    </main>
  </div>
</template>

<style>
/* You can move these to main.css or tailwind config if using Tailwind */
body {
  margin: 0;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  background-color: #FEF2F2;
  color: #7F1D1D;
}

/* Optional: Custom scrollbar */
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
