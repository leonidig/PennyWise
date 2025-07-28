<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWalletStore } from '@/stores/wallets'
import { useTransactionStore } from '@/stores/transactions'

const wallets = useWalletStore()
wallets.fetchWallets()
wallets.fetchCurrencies()
const transactions = useTransactionStore()
const router = useRouter()
const auth = useAuthStore()
const currencies = wallets.currencies
const balances = wallets.balances

</script>




<template>
  <div class="wallets-container">
    <h1>Wallets</h1>
    <div class="wallets-list">
      <div v-for="wallet in balances" :key="wallet.id" class="wallet-item">
        <h2>{{ wallet.name }}</h2>
        <p>Balance: {{ wallet.balance }} {{ currencies.find(c => c.id === wallet.currency).code }}</p>
        <button @click="router.push(`/wallets/${wallet.id}`)">View Details</button>
        <button @click="router.push(`/wallets/edit/${wallet.id}`)">Edit</button>
        <button @click="wallets.deleteWallet(wallet.id)">Delete</button>
      </div>
    </div>
    <button @click="router.push('/wallets/add')">Add New Wallet</button>
  </div>
</template>
