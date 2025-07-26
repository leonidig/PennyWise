<script setup>
import { ref } from 'vue'
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

const categories = categoriesStore.categories




const transactionsList = transactionsStore.transactions

</script>


<template>
  <div class="transactions-container">
    <h1>Transactions</h1>
    <div class="transactions-list">
      <div v-for="transaction in transactionsList" :key="transaction.id" class="transaction-item">
        <router-link to="/transactions/${transaction.id}"><h2>{{ categories.find(c => c.id === transaction.category).name }}</h2></router-link>
        <h3>Wallet: {{ balances[transaction.wallet-1]['name'] }} ({{ balances.find(w => w.id === transaction.wallet).balance }} {{ currencies.find(c => c.id === balances.find(w => w.id === transaction.wallet).currency).code }})</h3>
        <p>Amount: {{ transaction.amount }} {{ transaction.currency }}</p>
        <p>Comment: {{ transaction.comment }}</p>
        <p>Date: {{ new Date(transaction.created_at).toLocaleDateString() }}</p>
        <button @click="router.push(`/transactions/${transaction.id}/edit`)">Edit</button>
      </div>
    </div>
    <button @click="router.push('/transactions/add')">Add New Transaction</button>
  </div>

</template>
