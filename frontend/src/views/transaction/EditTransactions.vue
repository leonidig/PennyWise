<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTransactionStore } from '@/stores/transactions.js'
import { useWalletStore } from '@/stores/wallets.js'
import { useCategoryStore } from '@/stores/categories.js'

const route = useRoute()
const router = useRouter()
const transactionId = Number(route.params.id)

const loading = ref(false)
const error = ref(null)
const success = ref(false)

const transactionStore = useTransactionStore()
const walletStore = useWalletStore()
const categoryStore = useCategoryStore()

const wallets = ref([])
const categories = ref([])

const form = reactive({
  walletId: null,
  categoryId: null,
  amount: 0,
  comment: '',
})

onMounted(async () => {
  loading.value = true
  error.value = null
  success.value = false

  try {
    await walletStore.fetchWallets()
    await categoryStore.fetchCategories()
    wallets.value = walletStore.balances
    categories.value = categoryStore.categories

    const transaction = await transactionStore.getTransactionById(transactionId)
    if (!transaction) throw new Error('Transaction not found')

    form.walletId = transaction.wallet
    form.categoryId = transaction.category
    form.amount = transaction.amount
    form.comment = transaction.comment || ''
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const currencies = computed(() => walletStore.currencies)

async function handleSubmit() {
  error.value = null
  success.value = false

  if (!form.walletId || !form.categoryId || form.amount < 0) {
    error.value = 'Please fill in all required fields with valid values.'
    return
  }

  loading.value = true
  try {
    await transactionStore.updateTransaction(
      transactionId,
      form.walletId,
      form.amount,
      form.comment,
      form.categoryId
    )
    success.value = true
    router.push('/transactions')  // Navigate after successful update
  } catch (e) {
    error.value = e.message || 'Failed to update transaction.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="update-transaction-form">
    <div>
      <label for="wallet">Wallet:</label>
      <select id="wallet" v-model="form.walletId" required>
        <option v-for="wallet in wallets" :key="wallet.id" :value="wallet.id">
          {{ wallet.name }} ({{ currencies.find(c => c.id === wallet.currency)?.code || 'N/A' }})
        </option>
      </select>
    </div>

    <div>
      <label for="category">Category:</label>
      <select id="category" v-model="form.categoryId" required>
        <option v-for="category in categories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>
    </div>

    <div>
      <label for="amount">Amount:</label>
      <input
        id="amount"
        type="number"
        step="0.01"
        v-model.number="form.amount"
        required
        min="0"
      />
    </div>

    <div>
      <label for="comment">Comment:</label>
      <textarea id="comment" v-model="form.comment" placeholder="Optional comment"></textarea>
    </div>

    <button type="submit" :disabled="loading">Update Transaction</button>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">Transaction updated successfully!</p>
  </form>
  <p>
    <router-link :to="`/transactions/${transactionId}`">Back to Transaction Details</router-link>
  </p>
</template>

<style scoped>
.update-transaction-form {
  max-width: 480px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fafafa;
}
.update-transaction-form div {
  margin-bottom: 15px;
}
.update-transaction-form label {
  font-weight: 600;
  display: block;
  margin-bottom: 5px;
}
.update-transaction-form input,
.update-transaction-form select,
.update-transaction-form textarea {
  width: 100%;
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid #aaa;
  font-size: 1rem;
  box-sizing: border-box;
}
.update-transaction-form button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
}
.update-transaction-form button:disabled {
  background-color: #999;
  cursor: not-allowed;
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
</style>
