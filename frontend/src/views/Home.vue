<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ItemCarousel from '@/components/ItemCarousel.vue'
import Navbar from '@/components/Navbar.vue'

const router = useRouter()
const auth = useAuthStore()

const balances  = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/balances/')
    if (!response.ok) throw new Error('Failed to fetch')
    balances.value = await response.json()
  } catch (error) {
    console.error('Error fetching tips:', error)
    balances.value = [
      { name: 'Error fetching balance, please try again later', type: 'N/A', number: 'N/A', balance: 'N/A' },
    ]
  } finally {
    loading.value = false
  }
})
</script>

<template>
<Navbar />
<h1>Welcome!</h1>
<h3>Total Net Worth: </h3>
<h4>Your Balances</h4>
<h5 v-if="loading">Loading Balances...</h5>
<ItemCarousel :items="balances">
  <template #default="{ item }">
    <div class="balance-item">
      <p><strong>Name:</strong> {{ item.name }}</p>
      <p><strong>Type:</strong> {{ item.type }}</p>
      <p><strong>Number:</strong> {{ item.number }}</p>
      <p><strong>Balance:</strong> {{ item.balance }}</p>
    </div>
  </template>
</ItemCarousel>
</template>
