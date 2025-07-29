<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionStore } from '@/stores/transactions'
import { useWalletStore } from '@/stores/wallets'
import { useCategoryStore } from '@/stores/categories'

const router = useRouter()
const transactionsStore = useTransactionStore()
const walletsStore = useWalletStore()
const categoriesStore = useCategoryStore()

const loading = ref(true)
const error = ref(null)

const categories = computed(() => categoriesStore.categories)
const balances = computed(() => walletsStore.balances)
const currencies = computed(() => walletsStore.currencies)
const transactionsList = computed(() => transactionsStore.transactions)

async function fetchAll() {
  loading.value = true
  error.value = null
  try {
    await Promise.all([
      walletsStore.fetchWallets(),
      walletsStore.fetchCurrencies(),
      categoriesStore.fetchCategories(),
      transactionsStore.fetchTransactions()
    ])
  } catch (e) {
    error.value = 'Failed to load data.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAll()
})

const getCategory = (categoryId) => {
  return categories.value?.find(c => c.id == categoryId)
}

const getWallet = (walletId) => {
  return balances.value.find(w => w.id === walletId)
}


const getCurrencyCode = (walletId) => {
  const wallet = getWallet(walletId)
  if (!wallet) return ''
  const currency = currencies.value.find(c => c.id === wallet.currency)
  return currency?.code ?? ''
}

const deleteTransaction = async (id) => {
  try {
    await transactionsStore.deleteTransaction(id)
    await transactionsStore.fetchTransactions()
  } catch (err) {
    console.error('Error deleting transaction:', err)
  }
}
</script>

<template>
  <div class="transactions-container">
    <h1>Transactions</h1>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading">Loading transactions...</p>

    <div v-if="!loading && !error" class="transactions-list grid-4-cols">
      <div v-for="transaction in transactionsList" :key="transaction.id" class="transaction-item">
        <router-link :to="`/transactions/${transaction.id}`" class="transaction-link">
          <p :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' }">
            {{ getCategory(transaction.category)?.name || 'Unknown' }}
          </p>
          <p class="badge" :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' }">
            Amount: {{ transaction.amount }} {{ getCurrencyCode(transaction.wallet) }}
          </p>
        </router-link>
        <h3>
          Wallet: {{ getWallet(transaction.wallet)?.name || 'Unknown Wallet' }}
          ({{ getWallet(transaction.wallet)?.balance ?? '-' }} {{ getCurrencyCode(transaction.wallet) }})
        </h3>
        <p>Comment: {{ transaction.comment || 'No comment' }}</p>
        <p class="transaction-date">
              {{ new Date(transaction.created_at).toLocaleString('en-US', {
                weekday: 'short',
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              }) }}
            </p>
        <button @click="router.push(`/transactions/${transaction.id}/edit`)">Edit</button>
        <button @click="deleteTransaction(transaction.id)">Delete</button>
      </div>
    </div>
    <button @click="router.push('/transactions/add')" class="add-btn">Add New Transaction</button>
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
.transactions-container {
  margin: 20px auto;
  padding: 15px 20px;
  font-family: Arial, sans-serif;
}

.transaction-link {
  text-decoration: none;
}

.badge {
  font-weight: 700;
  background-color: #e0e7ff;
  border-radius: 15px;
  padding: 5px 12px;
  display: inline-block;
  margin-top: 5px;
}

button {
  margin: 8px 10px 0 0;
  padding: 6px 14px;
  border-radius: 4px;
  border: none;
  background-color: #1976d2;
  color: white;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #1565c0;
}

.add-btn {
  margin-top: 15px;
}

.error {
  color: red;
  font-weight: 600;
  margin-bottom: 15px;
}
</style>
