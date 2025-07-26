<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWalletStore } from '@/stores/wallets'
import ItemCarousel from '@/components/ItemCarousel.vue'
import { useTransactionStore } from '@/stores/transactions'
import RecentTransactions from '@/components/RecentTransactions.vue'

const router = useRouter()
const auth = useAuthStore()
const wallets = useWalletStore()
const transactions = useTransactionStore()

const balances = ref([])
const currencies = ref([])
const transactionsList = ref([])
const inverseRates = ref({})
const loading = ref(true)

onMounted(async () => {
  try {

    await wallets.fetchWallets()
    await wallets.fetchCurrencies()
    await transactions.fetchTransactions()

    balances.value = wallets.balances
    currencies.value = wallets.currencies
    transactionsList.value = transactions.transactions

    if (!currencies.value.length) {
      console.warn('No currencies loaded — skipping exchange rate fetch')
      return
    }

    const currenciesUsed = currencies.value.map(c => c.code).join(',')
    const rateRes = await fetch(
      `https://api.exchangerate.host/live?access_key=bcdae7fbdec58e47ad6d16dede76db0c&source=EUR&currencies=${currenciesUsed}`
    )
    const rateData = await rateRes.json()

    console.log('Exchange rate response:', rateData)
    console.log('Balances:', balances.value)
    console.log('Currencies:', currencies.value)


    for (const [key, value] of Object.entries(rateData.quotes)) {
      const currency = key.replace('EUR', '')
      inverseRates.value[currency] = 1 / value
    }
    console.log('Inverse Rates:', inverseRates.value)

  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
})

// Compute total in EUR
const totalInEUR = computed(() => {
  if (!balances.value.length || !Object.keys(inverseRates.value).length) return 0

  return balances.value.reduce((sum, wallet) => {
    const currencyCode = currencies.value.find(c => c.id == wallet.currency)?.code
    if (!currencyCode) return sum

    const balanceNum = Number(wallet.balance)
    if (isNaN(balanceNum)) return sum

    if (currencyCode === 'EUR') {
      return sum + balanceNum
    }

    const rate = Number(inverseRates.value[currencyCode])
    if (isNaN(rate)) return sum

    return sum + balanceNum * rate
  }, 0)
})



const formattedTotalInEUR = computed(() => {
  const total = totalInEUR.value
  console.log('Total in EUR:', total)
  if (typeof total !== 'number' || isNaN(total)) return '€0.00'

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'EUR'
  }).format(total)
})




</script>

<template>
  <h1>Welcome!</h1>
  <h3>Total Balance Worth: {{ formattedTotalInEUR }} EUR</h3>

  <h4>Your Balances</h4>
  <h5 v-if="loading">Loading...</h5>
  <ItemCarousel v-if="!loading && balances.length" :items="balances" />
  <h5 v-else>No balances found.</h5>

  <h3>Recent Transactions</h3>
  <RecentTransactions :items="transactionsList" />
</template>
