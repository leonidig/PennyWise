<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionStore } from '@/stores/transactions'
import { useCategoryStore } from '@/stores/categories'
import { useWalletStore } from '@/stores/wallets'

const router = useRouter()
const transactions = useTransactionStore()
const categories = useCategoryStore()
const wallets = useWalletStore()

const error = ref('')
const amount = ref(null)
const categoryId = ref(null)
const walletId = ref(null)
const comment = ref('')

const loading = ref(true)
const submitting = ref(false)

onMounted(async () => {
  try {
    await Promise.all([
      categories.fetchCategories(),
      wallets.fetchWallets(),
      wallets.fetchCurrencies(),
    ])
  } finally {
    loading.value = false
  }
})

async function addTransaction() {
  error.value = ''
  if (amount.value === null || amount.value <= 0) {
    error.value = 'Please enter a positive amount'
    return
  }
  if (!categoryId.value || !walletId.value) {
    error.value = 'Please select both category and wallet'
    return
  }
  submitting.value = true
  try {
    await transactions.addTransaction(
      walletId.value,
      parseFloat(amount.value),
      comment.value,
      categoryId.value,
    )
    router.push('/transactions')
  } catch (err) {
    console.error('Error adding transaction:', err)
    error.value = 'Failed to add transaction. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="add-transaction-container">
    <h1>Add Transaction</h1>

    <div v-if="loading">Loading data...</div>

    <form v-else @submit.prevent="addTransaction">
      <div class="form-group">
        <label for="amount">Amount:</label>
        <input
          type="number"
          id="amount"
          v-model.number="amount"
          min="0.01"
          step="0.01"
          required
          :disabled="submitting"
        />
      </div>

      <div class="form-group">
        <label for="category">Category:</label>
        <select id="category" v-model="categoryId" required :disabled="submitting">
          <option disabled value="">Select category</option>
          <option
            v-for="category in categories.categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="comment">Comment:</label>
        <input
          type="text"
          id="comment"
          v-model="comment"
          placeholder="Optional comment"
          :disabled="submitting"
        />
      </div>

      <div class="form-group">
        <label for="wallet">Wallet:</label>
        <select id="wallet" v-model="walletId" required :disabled="submitting">
          <option disabled value="">Select wallet</option>
          <option
            v-for="wallet in wallets.balances"
            :key="wallet.id"
            :value="wallet.id"
          >
            {{ wallet.name }} ({{ wallet.balance }} {{
              wallets.currencies.find(c => c.id === wallet.currency)?.code || 'N/A'
            }})
          </option>
        </select>
      </div>

      <button type="submit" :disabled="submitting">
        {{ submitting ? 'Adding...' : 'Add Transaction' }}
      </button>
    </form>

    <p v-if="error" style="color: red;">{{ error }}</p>

    <p>Go back to <router-link to="/transactions">Transactions</router-link>.</p>
  </div>
</template>



<style scoped>
.add-transaction-container {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fafafa;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 5px;
}

input[type="number"],
input[type="text"],
select {
  width: 100%;
  padding: 8px 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 15px;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: #155fa0;
}

button:disabled {
  background-color: #a1a1a1;
  cursor: not-allowed;
}

p {
  margin-top: 15px;
}
</style>
