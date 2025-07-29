<script setup>
import { ref, computed, watchEffect, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTransactionStore } from '@/stores/transactions'
import { useWalletStore } from '@/stores/wallets'
import { useCategoryStore } from '@/stores/categories'

const route = useRoute()
const router = useRouter()

const transactions = useTransactionStore()
const wallets = useWalletStore()
const categories = useCategoryStore()

const error = ref('')
const amount = ref('')
const categoryId = ref(null)
const walletId = ref(null)
const comment = ref('')
const wallet = ref(null)
const currency = ref('')


onMounted(async () => {
  try {
    await transactions.fetchTransactions()
    await wallets.fetchWallets()
    await wallets.fetchCurrencies()
    await categories.fetchCategories()
  } catch (err) {
    error.value = 'Failed to load data.'
  }
})

const currencies = wallets.currencies
const categoriesList = computed(() => categories.categories)

const transaction = computed(() =>
  transactions.transactions.find(t => t.id == route.params.id)
)

watchEffect(() => {
  if (transaction.value) {
    amount.value = transaction.value.amount
    categoryId.value = transaction.value.category
    walletId.value = transaction.value.wallet
    comment.value = transaction.value.comment || ''

    wallet.value = wallets.balances.find(w => w.id === walletId.value)
    currency.value = currencies.find(c => c.id === wallet.value?.currency)?.code ?? ''

    error.value = ''
  } else {
    error.value = 'Transaction not found or still loading.'
  }
})

const getCategory = (categoryId) => {
  return categoriesList.value?.find(c => c.id == categoryId)
}

const deleteTransaction = async (id) => {
  try {
    await transactions.deleteTransaction(id)
    await transactions.fetchTransactions()
    router.push('/transactions')
  } catch (err) {
    console.error('Error deleting transaction:', err)
    error.value = 'Failed to delete transaction. Please try again.'
  }
}



</script>

<template>
  <div class="transaction-info-container">
    <h1>Transaction Details</h1>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-else>
      <h2>Transaction ID: {{ route.params.id }}</h2>
      <h3>Date: {{ transaction ? new Date(transaction.created_at).toLocaleDateString('en-US', {
                weekday: 'short',
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              }) : 'Loading...' }}
              </h3>
      <h4>Wallet: {{ wallet?.name }} ({{ wallet?.balance }} {{ currency }})</h4>

      <div class="transaction-details">
        <p :style="{ color: getCategory(categoryId)?.is_income ? 'green' : 'red' }">
          Category: {{ getCategory(categoryId)?.name || 'Unknown' }}
        </p>
        <p class="badge" :style="{ color: getCategory(categoryId)?.is_income ? 'green' : 'red' }">
          Amount: {{ amount }} {{ currency }}
        </p>
        <p>Comment: {{ comment || 'No comment provided' }}</p>
      </div>

      <button @click="router.push(`/transactions/${route.params.id}/edit`)">Edit Transaction</button>
      <button @click="deleteTransaction(route.params.id)">Delete</button>
      <button @click="router.push('/transactions')">Back to Transactions</button>
    </div>
  </div>
</template>

<style scoped>
.transaction-info-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 15px 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  font-family: Arial, sans-serif;
}

.transaction-info-container h1 {
  margin-bottom: 20px;
  text-align: center;
}

.transaction-details {
  margin: 15px 0;
  padding: 10px;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
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
  margin: 10px 8px 0 0;
  padding: 8px 15px;
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

.error {
  color: red;
  font-weight: 600;
  text-align: center;
  margin-bottom: 15px;
}
</style>
