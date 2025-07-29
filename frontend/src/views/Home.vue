<template>
  <div class="home-container">
    <div class="becentre">
    <div class="section-card">
      <h1 class="section-title">Welcome!</h1>
      <h3 class="section-subtitle">Total Balance Worth</h3>
      <p class="balance-total">{{ formattedTotalInEUR }} EUR</p>
    </div>

    <div class="section-card">
      <h3 class="section-subtitle">Your Balances</h3>
      <div v-if="loading" class="loading-msg">Loading your wallets...</div>
      <ItemCarousel v-else-if="balances.length" :items="balances" />
      <div v-else class="no-data-msg">No balances found.</div>
    </div>

    <div class="section-card">
      <h3 class="section-subtitle">Recent Transactions</h3>
      <RecentTransactions :items="transactionsList" />
    </div>
  </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useWalletStore } from '@/stores/wallets'
import { useTransactionStore } from '@/stores/transactions'
import ItemCarousel from '@/components/ItemCarousel.vue'
import RecentTransactions from '@/components/RecentTransactions.vue'

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

    // const currenciesUsed = currencies.value.map(c => c.code).join(',')
    // const rateRes = await fetch(
    //   `https://api.exchangerate.host/live?access_key=bcdae7fbdec58e47ad6d16dede76db0c&source=EUR&currencies=${currenciesUsed}`
    // )
    // const rateData = await rateRes.json()

    const rateData = {
      success: true,
      quotes: {
        'EURUSD': 1.1,
        'EURBTC': 0.9,
        'EURUAH': 130.0
      }
    }

    for (const [key, value] of Object.entries(rateData.quotes)) {
      const currency = key.replace('EUR', '')
      inverseRates.value[currency] = 1 / value
    }
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
})

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
  if (typeof total !== 'number' || isNaN(total)) return '€0.00'

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'EUR'
  }).format(total)
})
</script>

<style scoped>
.home-container {
  width: 1300px;
  padding: 0rem 2rem;
  display: flex;
  gap: 1.5rem;
  box-sizing: border-box;
}

.becentre {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
}



.section-card {
  width: 100%;
  background: #FEF2F2;
  border: 2px solid #F87171;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);

}




.section-title {
  font-size: 2rem;
  color: #DC2626;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.balance-total {
  font-size: 1.5rem;
  font-weight: bold;
  color: #7F1D1D;
}

.loading-msg {
  color: #DC2626;
  font-weight: 500;
}

.no-data-msg {
  color: #9CA3AF;
  font-style: italic;
}
</style>
