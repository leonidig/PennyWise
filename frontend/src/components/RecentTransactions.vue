<template>
  <div class="transactions-card" v-if="categories.length && wallets.length && currencies.length">
    <div class="transactions-header">
      <button
        :class="['filter-btn', { active: transaction_type === 'All' }]"
        @click="transaction_type = 'All'"
      >All</button>
      <button
        :class="['filter-btn', { active: transaction_type === 'Incomes' }]"
        @click="transaction_type = 'Incomes'"
      >Incomes</button>
      <button
        :class="['filter-btn', { active: transaction_type === 'Expenses' }]"
        @click="transaction_type = 'Expenses'"
      >Expenses</button>
    </div>

    <div class="transactions-body">
      <div class="transactions-list grid-4-cols">
        <div
          v-for="item in filteredItems.slice(0, 10)"
          :key="item.id"
          class="transaction-item"
        >
          <router-link :to="`/transactions/${item.id}`" class="transaction-link">
            <div class="transaction-row">
              <span
                class="transaction-category"
                :class="{
                  income: getCategory(item.category)?.is_income,
                  expense: !getCategory(item.category)?.is_income
                }"
              >
                {{ getCategory(item.category)?.name || 'Unknown' }}
              </span>

              <span
                class="transaction-amount"
                :class="{
                  income: getCategory(item.category)?.is_income,
                  expense: !getCategory(item.category)?.is_income
                }"
              >
                {{ item.amount }} {{ getCurrencyCode(item.wallet) }}
              </span>
            </div>

            <small class="transaction-date">
              {{ new Date(item.created_at).toLocaleString('en-US', {
                weekday: 'short',
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              }) }}
            </small>
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <div v-else>Loading...</div>
</template>

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
})

const transaction_type = ref('All')

const sortedItems = computed(() =>
  [...props.items].sort((a, b) => new Date(b.date) - new Date(a.date))
)

const filteredItems = computed(() => {
  if (categories.value.length === 0) return []
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
  if (!wallet) return 'Unknown'
  const currency = currencies.value.find(c => c.id === wallet.currency)
  return currency?.code || 'Unknown'
}

const getCategory = (categoryId) =>
  categories.value?.find(c => c.id == categoryId)
</script>

<style>
.grid-4-cols {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.transaction-item {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.transactions-card {
  background: #FEF2F2;
  border: 2px solid #F87171;
  border-radius: 10px;
  padding: 1.5rem;
  margin: 2rem auto;
  color: #7F1D1D;
  font-family: 'Segoe UI', sans-serif;
  box-shadow: 0 4px 8px rgba(220, 38, 38, 0.1);
}

.transactions-header {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #DC2626;
  background-color: white;
  color: #DC2626;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s ease;
}

.filter-btn:hover {
  background-color: #FECACA;
}

.filter-btn.active {
  background-color: #DC2626;
  color: white;
}

.transactions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.transaction-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.transaction-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.transaction-category {
  font-weight: 600;
}

.transaction-amount {
  font-weight: bold;
}

.transaction-category.income,
.transaction-amount.income {
  color: #15803D;
}

.transaction-category.expense,
.transaction-amount.expense {
  color: #DC2626;
}

.transaction-date {
  font-size: 0.8rem;
  color: #6B7280;
}
</style>
