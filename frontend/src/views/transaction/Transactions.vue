<script setup>
import { ref, computed } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useTransactionStore } from '@/stores/transactions'
import { useWalletStore } from '@/stores/wallets'
import { useCategoryStore } from '@/stores/categories'

const router = useRouter()
const wallets = useWalletStore()
wallets.fetchWallets()
wallets.fetchCurrencies()
const transactionsStore = useTransactionStore()
const balances = wallets.balances
const currencies = wallets.currencies
const categoriesStore = useCategoryStore()
categoriesStore.fetchCategories()

const categories = computed(() => categoriesStore.categories)




const transactionsList = transactionsStore.transactions

const getCategory = (categoryId) => {
  return categories.value?.find(c => c.id == categoryId)
}

const deleteTransaction = async (id) => {
  try {
    await transactionsStore.deleteTransaction(id)
    transactionsStore.fetchTransactions()
    router.push('/transactions')
  } catch (err) {
    console.error('Error deleting transaction:', err)
  }
}

</script>


<template>
  <div class="transactions-container">
    <h1>Transactions</h1>
    <div class="transactions-list">
      <div v-for="transaction in transactionsList" :key="transaction.id" class="transaction-item">
        <router-link :to="`/transactions/${transaction.id}`">
          <p :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' } ">
            {{ getCategory(transaction.category)?.name || 'Unknown' }}
          </p>
          <p class="badge bg-primary rounded-pill" :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' }">
            Amount: {{ transaction.amount }} {{ currencies.find(c => c.id === balances.find(w => w.id === transaction.wallet).currency).code }}
          </p>
        </router-link>
        <h3>Wallet: {{ balances.find(n => n.id === transaction.wallet).name }} ({{ balances.find(w => w.id === transaction.wallet).balance }} {{ currencies.find(c => c.id === balances.find(w => w.id === transaction.wallet).currency).code }})</h3>
        <p>Comment: {{ transaction.comment || 'No comment' }}</p>
        <p>Date: {{ new Date(transaction.created_at).toLocaleDateString() }}</p>
        <button @click="router.push(`/transactions/${transaction.id}/edit`)">Edit</button>
        <button @click="deleteTransaction(transaction.id)">Delete</button>
      </div>
    </div>
    <button @click="router.push('/transactions/add')">Add New Transaction</button>
  </div>

</template>
