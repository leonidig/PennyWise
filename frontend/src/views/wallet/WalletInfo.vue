<script setup>
import { ref, computed } from 'vue'
import { useWalletStore } from '@/stores/wallets'
import { useTransactionStore } from '@/stores/transactions'
import { useRoute, useRouter } from 'vue-router'
import { useCategoryStore } from '@/stores/categories'

const route = useRoute()
const router = useRouter()

const wallets = useWalletStore()
const transactions = useTransactionStore()
const categoryStore = useCategoryStore()

const selectedCategory = ref('')
const searchQuery = ref('')
const transaction_type = ref('')

const wallet = computed(() =>
  wallets.balances.find(w => w.id == route.params.id)
)

const transactionsList = computed(() =>
  wallet.value
    ? transactions.transactions.filter(t => t.wallet === wallet.value.id)
    : []
)


const sortedItems = computed(() =>
  transactionsList.value.sort((a, b) => new Date(b.date) - new Date(a.date))
)

const getCategory = (categoryId) => {
  return categories.value?.find(c => c.id === categoryId)
}

const filteredTransactions = computed(() => {
  return sortedItems.value.filter((t) => {
    const category = getCategory(t.category)
    const matchesCategory = selectedCategory.value
      ? category?.id === parseInt(selectedCategory.value)
      : true
    const matchesSearch = t.comment?.toLowerCase().includes(searchQuery.value.toLowerCase()) || ''
    if (transaction_type.value === 'Incomes') return category.is_income && matchesCategory && matchesSearch
    if (transaction_type.value === 'Expenses') return !category.is_income && matchesCategory && matchesSearch
    return matchesCategory && matchesSearch
  })
})

const currencies = computed(() => wallets.currencies)

const categories = computed(() => categoryStore.categories)




const currencyCode = computed(() => {
  if (!wallet.value) return ''
  const c = currencies.value.find(c => c.id === wallet.value.currency)
  return c?.code || ''
})

const deletingWallet = ref(false)
const deletingTransactionIds = ref(new Set())

async function confirmAndDeleteWallet() {
  if (!wallet.value) return
  if (confirm(`Are you sure you want to delete wallet "${wallet.value.name}"? This action cannot be undone.`)) {
    deletingWallet.value = true
    try {
      await wallets.deleteWallet(wallet.value.id)
      router.push('/wallets')
    } catch (error) {
      alert('Failed to delete wallet.')
      console.error(error)
    } finally {
      deletingWallet.value = false
    }
  }
}

async function confirmAndDeleteTransaction(id) {
  if (confirm('Are you sure you want to delete this transaction?')) {
    deletingTransactionIds.value.add(id)
    try {
      await transactions.deleteTransaction(id)
    } catch (error) {
      alert('Failed to delete transaction.')
      console.error(error)
    } finally {
      deletingTransactionIds.value.delete(id)
    }
  }
}
</script>

<template>
  <div class="wallet-info-container" v-if="wallet">
    <h1>{{ wallet.name }}</h1>
    <p>
      Balance: {{ wallet.balance }} {{ currencyCode }}
    </p>
    <p>Currency: {{ currencyCode }}</p>
    <button @click="router.push(`/wallets/edit/${wallet.id}`)" :disabled="deletingWallet">
      Edit Wallet
    </button>
    <button @click="confirmAndDeleteWallet" :disabled="deletingWallet">
      {{ deletingWallet ? 'Deleting...' : 'Delete Wallet' }}
    </button>

    <h2>Wallet Transactions</h2>

      <div class="filter-controls" v-if='sortedItems.length'>
        <select v-model="selectedCategory">
          <option value="">All Categories</option>
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
        <input v-model="searchQuery" placeholder="Search by comment..." />
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
          </div>

    <div class="transactions-list grid-4-cols">
      <div
        v-for="transaction in filteredTransactions"
        :key="transaction.id"
        class="transaction-item"
      >
        <router-link :to="`/transactions/${transaction.id}`">
          <p
            :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' }"
          >
            {{ getCategory(transaction.category)?.name || 'Unknown' }}
          </p>
          <p
            class="badge bg-primary rounded-pill"
            :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' }"
          >
            Amount: {{ transaction.amount }} {{ currencyCode }}
          </p>
        </router-link>
        <p>Comment: {{ transaction.comment || 'No comment' }}</p>
        <p>Date: {{ new Date(transaction.created_at).toLocaleDateString() }}</p>
        <button
          @click="router.push(`/transactions/${transaction.id}/edit`)"
          :disabled="deletingTransactionIds.has(transaction.id)"
        >
          Edit
        </button>
        <button
          @click="confirmAndDeleteTransaction(transaction.id)"
          :disabled="deletingTransactionIds.has(transaction.id)"
        >
          {{ deletingTransactionIds.has(transaction.id) ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </div>

    <button @click="router.push('/transactions/add')">Add New Transaction</button>
  </div>

  <div v-else>
    <p>Loading wallet information...</p>
  </div>
</template>

<style scoped>
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
.wallet-info-container {
  max-width: none;
  margin: 2rem auto;
  padding: 1rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.transactions-list {
  margin-top: 1rem;
}

.transaction-item p {
  margin: 0.25rem 0;
}

button {
  margin-right: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.filter-controls {
  margin-bottom: 16px;
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-controls input,
.filter-controls select {
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
