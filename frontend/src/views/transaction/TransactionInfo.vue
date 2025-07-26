<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionStore } from '@/stores/transactions'
import { useWalletStore } from '@/stores/wallets'
import { useCategoryStore } from '@/stores/categories'

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
const currencies = wallets.currencies
const currency = ref('')

const transaction = transactions.getTransactionById(router.currentRoute.value.params.id)
if (transaction) {
  amount.value = transaction.amount
  categoryId.value = transaction.category
  walletId.value = transaction.wallet
  comment.value = transaction.comment

} else {
  error.value = 'Transaction not found.'
}

wallet.value = wallets.getWalletById(transaction.wallet)
currency.value = currencies[wallet.value.currency - 1]['code']


</script>


<template>
<h1>{{ comment }}</h1>
<h2>Amount: {{ amount }} {{ currency }}</h2>
<h3>Category: {{ categories.categories.find(cat => cat.id === categoryId)?.name }}</h3>
<h4>Wallet: {{ wallet?.name }} ({{ wallet?.balance }} {{ currency }})</h4>
<p v-if="error" style="color: red;">{{ error }}</p>
<button @click="router.push(`/transactions/${router.currentRoute.value.params.id}/edit`)">Edit Transaction</button>
<button @click="router.push('/transactions')">Back to Transactions</button>

</template>
