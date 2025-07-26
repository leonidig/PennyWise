<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionStore } from '@/stores/transactions'
import { useCategoryStore } from '@/stores/categories'
import { useWalletStore } from '@/stores/wallets'

const router = useRouter()
const transactions = useTransactionStore()
const categories = useCategoryStore()
const wallets = useWalletStore()
const error = ref('')
const amount = ref('')
const categoryId = ref(null)
const walletId = ref(null)
const comment = ref('')





async function addTransaction() {
    try {
        await transactions.addTransaction(
            walletId.value,
            parseFloat(amount.value),
            comment.value ,
            categoryId.value,

        );

        router.push('/transactions');
    } catch (err) {
        console.error('Error adding transaction:', err);
        error.value = 'Failed to add transaction. Please try again.';
    }
}
</script>



<template>
  <div class="add-transaction-container">
    <h1>Add Transaction</h1>
    <form @submit.prevent="addTransaction">
      <div class="form-group">
        <label for="amount">Amount:</label>
        <input type="number" id="amount" v-model.number="amount" required>
      </div>
      <div class="form-group">
        <label for="category">Category:</label>
        <select id="category" v-model="categoryId" required>
          <option v-for="category in categories.categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="comment">Comment:</label>
        <input type="text" id="comment" v-model="comment" placeholder="Optional comment">
      </div>
      <div class="form-group">
        <label for="wallet">Wallet:</label>
        <select id="wallet" v-model="walletId" required>
          <option v-for="wallet in wallets.balances" :key="wallet.id" :value="wallet.id">{{ wallet.name }} ({{ wallet.balance }} {{ wallets.currencies.find(c => c.id ===wallet.currency).code }})</option>
        </select>
      </div>
      <button type="submit">Add Transaction</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
    <p>Go back to <router-link to="/transactions">Transactions</router-link>.</p>
  </div>
</template>
