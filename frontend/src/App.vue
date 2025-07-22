<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ItemCarousel from '@/components/ItemCarousel.vue'
import Navbar from '@/components/Navbar.vue'

const router = useRouter()
const auth = useAuthStore()
</script>

<template>
<Navbar />
<router-view />
</template>

<style>

</style>
