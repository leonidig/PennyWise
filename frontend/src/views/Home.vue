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
const currenciesUsed = ['EUR', 'USD', 'BTC', 'UAH']
const exchangeRates = ref({})



onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/wallets/')
    if (!response.ok) throw new Error('Failed to fetch')
    balances.value = await response.json()
    const rateRes = await fetch(
      `https://api.exchangerate.host/latest?base=EUR&symbols=${currenciesUsed.join(',')}`
    )
    const rateData = await rateRes.json()

    // Invert rates so you can convert from wallet currency → EUR
    for (const [currency, rate] of Object.entries(rateData.rates)) {
      exchangeRates.value[currency] = currency === 'EUR' ? 1 : 1 / rate
    }
  } catch (error) {
    console.error('Error loading data:', error)
    exchangeRates.value = { EUR: 1 }
  } finally {
    loading.value = false
  }
})

  

function convertToEUR(wallet) {
  const rate = exchangeRates.value[wallet.currency] ?? 1
  const raw = parseFloat(wallet.balance)
  return isNaN(raw) ? 0 : raw * rate
}

const totalNetWorthEUR = computed(() => {
  return balances.value.reduce((sum, wallet) => {
    return sum + convertToEUR(wallet)
  }, 0)
})

</script>

<template>
<h1>Welcome!</h1>
<h3>Total Net Worth: €{{ totalNetWorthEUR.toFixed(2) }}  EUR</h3>
<h4>Your Balances</h4>
<h5 v-if="loading">Loading Balances...</h5>
<ItemCarousel :items="balances">
  <template #default="{ item }">
    <div class="balance-item">
      <p><strong>Name:</strong> {{ item.name }}</p>
      <p><strong>Balance:</strong> {{ item.balance }} {{item.currency}}</p>
    </div>
  </template>
</ItemCarousel>
</template>
