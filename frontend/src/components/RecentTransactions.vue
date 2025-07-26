<script setup>

import { ref, computed, onMounted } from 'vue'
import { useCategoryStore } from '@/stores/categories'
import { useWalletStore } from '@/stores/wallets'

const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

const categoryStore = useCategoryStore()
const walletStore = useWalletStore()
const categories = ref([])
const wallets = ref([])
const currencies = ref([])

onMounted(async () => {
  await categoryStore.fetchCategories()
  await walletStore.fetchWallets()
  await walletStore.fetchCurrencies()
  wallets.value = walletStore.balances
  currencies.value = walletStore.currencies
  categories.value = categoryStore.categories
  console.log('Categories:', categories.value)
})







const transaction_type = ref('All')

const sortedItems = computed(() => {
  return [...props.items].sort((a, b) => new Date(b.date) - new Date(a.date))
})

const filteredItems = computed(() => {
  if (categories.value.length === 0) return [] // wait for categories
  return sortedItems.value.filter(item => {
    const category = categories.value.find(c => c.id === item.category)
    if (!category) return false
    if (transaction_type.value === 'Incomes') return category.is_income
    if (transaction_type.value === 'Expenses') return !category.is_income
    return true
  })
})


const getCurrencyCode = (walletId) => {
  const wallet = wallets.value.find(w => w.id === walletId)
  if (!wallet) return '???'
  const currency = currencies.value.find(c => c.id === wallet.currency)
  return currency?.code || '???'
}

const getCategory = (categoryId) => {
  return categories.value?.find(c => c.id === categoryId)
}


console.log('Filtered Items:', filteredItems.value)



</script>

<template>
<div class="card" v-if="categories.length && wallets.length && currencies.length">
  <div class="card-header">
    <button class="btn btn-primary" @click="transaction_type = 'All' "><h3 class="card-title">Recent Transactions</h3></button>
    <button class="btn btn-primary" @click="transaction_type = 'Incomes' "><h4 class="card-title">Incomes</h4></button>
    <button class="btn btn-primary" @click="transaction_type = 'Expenses' "><h4 class="card-title">Expenses</h4></button>
  </div>
  <div class="card-body">
    <ul class="list-group">
      <li v-for="(item) in filteredItems.slice(0,10)" :key="item.id" class="list-group-item">
        <router-link :to="`/transactions/${item.id}`"><div class="d-flex justify-content-between align-items-center">
          <p :style="{ color: getCategory(item.category)?.is_income ? 'green' : 'red' }">
              {{ getCategory(item.category)?.name || 'Unknown' }}
          </p>
          <p class="badge bg-primary rounded-pill">{{ item.amount }} {{ getCurrencyCode(item.wallet) }}</p>
        </div></router-link>
        <small class="text-muted">{{ new Date(item.created_at).toLocaleString('en-US',
        { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'}) }}
        </small>
      </li>
    </ul>
  </div>
</div>
<div v-else>
    Loading...
</div>
</template>
