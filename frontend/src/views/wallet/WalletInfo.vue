<script setup>
import { onMounted, ref, computed } from 'vue'
import { useWalletStore } from '@/stores/wallets'
import { useTransactionStore } from '@/stores/transactions'
import { useRoute, useRouter } from 'vue-router'
import { useCategoryStore } from '@/stores/categories'

const route = useRoute()
const router = useRouter()


const wallets = useWalletStore()
const transactions = useTransactionStore()
const categoryStore = useCategoryStore()

const wallet = computed(() =>
  wallets.balances.find(w => w.id == route.params.id)
)

const transactionsList = computed(() =>
  transactions.transactions.filter(t => t.wallet === wallet.value.id)

)

const currencies = computed(() =>
  wallets.currencies
)

const categories = computed(() =>
  categoryStore.categories
)

const getCategory = (categoryId) => {
  return categories.value?.find(c => c.id === categoryId)
}




</script>


<template>
  <div class="wallet-info-container">
    <h1>{{ wallet.name }}</h1>
    <p>Balance: {{ wallet.balance }} {{ currencies.find(c => c.id === wallet.currency).code }}</p>
    <p>Currency: {{ currencies.find(c => c.id === wallet.currency).code }}</p>
    <button @click="router.push(`/wallets/edit/${wallet.id}`)">Edit Wallet</button>
    <button @click="wallets.deleteWallet(wallet.id)">Delete Wallet</button>
    <p></p>
    <h2>Wallet Transactions</h2>
    <div class="transactions-list">
      <div v-for="transaction in transactionsList" :key="transaction.id" class="transaction-item">
        <router-link :to="`/transactions/${transaction.id}`">
          <p :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' } ">
            {{ getCategory(transaction.category)?.name || 'Unknown' }}
          </p>
          <p class="badge bg-primary rounded-pill" :style="{ color: getCategory(transaction.category)?.is_income ? 'green' : 'red' }">
            Amount: {{ transaction.amount }} {{ currencies.find(c => c.id === wallet.currency).code }}
          </p>
        </router-link>
        <p>Comment: {{ transaction.comment || 'No comment' }}</p>
        <p>Date: {{ new Date(transaction.created_at).toLocaleDateString() }}</p>
        <button @click="router.push(`/transactions/${transaction.id}/edit`)">Edit</button>
        <button @click="transactions.deleteTransaction(transaction.id)">Delete</button>
      </div>
    </div>
    <button @click="router.push('/transactions/add')">Add New Transaction</button>
  </div>
</template>
