<script setup>
import Navbar from '@/components/NavbarComp.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const hideNavbarOn = ['/login', '/register']
</script>

<template>
  <div class="bg-red-50 text-red-900 font-sans w-full min-h-screen">
    <Navbar v-if="!hideNavbarOn.includes(route.path)" />
    <main class="main-content">
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

.main-content {
  padding: 6rem 2rem 2rem;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
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
