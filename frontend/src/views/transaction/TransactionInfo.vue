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
  await transactions.fetchTransactions()
  await wallets.fetchWallets()
  await wallets.fetchCurrencies()
  await categories.fetchCategories()
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
    comment.value = transaction.value.comment

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
    transactions.fetchTransactions()
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
      <h3>Date: {{ new Date(transaction?.created_at).toLocaleDateString() }}</h3>
    </div>
    <h4>Wallet: {{ wallet?.name }} ({{ wallet?.balance }} {{ currency }})</h4>
    <div class="transaction-details">
      <p :style="{ color: getCategory(categoryId)?.is_income ? 'green' : 'red' }">
        Category: {{ getCategory(categoryId)?.name || 'Unknown' }}
      </p>
      <p class="badge bg-primary rounded-pill" :style="{ color: getCategory(categoryId)?.is_income ? 'green' : 'red' }">
        Amount: {{ amount }} {{ currency }}
      </p>
      <p>Comment: {{ comment || 'No comment provided' }}</p>
    </div>
    <button @click="router.push(`/transactions/${route.params.id}/edit`)">Edit Transaction</button>
    <button @click="deleteTransaction(route.params.id)">Delete</button>
    <button @click="router.push('/transactions')">Back to Transactions</button>
  </div>
</template>

