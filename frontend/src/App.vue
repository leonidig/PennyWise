<script setup>
import Navbar from '@/components/NavbarComp.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const hideNavbarOn = ['/login', '/register']

</script>

<template>
  <Navbar v-if="!hideNavbarOn.includes(route.path)" />
  <router-view />
</template>

<style>


</style>
