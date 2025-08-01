<template>
  <div class="layout-wrapper">
    <Navbar v-if="!hideNavbarOn.includes(route.path)" />
    <main
      :class="['main-content', { 'with-navbar': !hideNavbarOn.includes(route.path) }]"
    >
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Navbar from '@/components/NavbarComp.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const hideNavbarOn = ['/login', '/register']
</script>

<style>
body, html {
  margin: 0;
  height: 100%;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  background-color: #FEF2F2;
  color: #7F1D1D;
}

.layout-wrapper {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #FEF2F2;
}

.main-content {
  flex-grow: 1;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem;
  min-height: calc(100vh - 0px);
}

.main-content.with-navbar {
  padding-top: 6rem;
  min-height: calc(100vh - 6rem);
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
