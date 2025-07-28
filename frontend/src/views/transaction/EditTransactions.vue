<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTransactionStore } from '@/stores/transactions.js'
import { useWalletStore } from '@/stores/wallets.js'
import { useCategoryStore } from '@/stores/categories.js'
import router from '@/router'

const route = useRoute()
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
  } catch (e) {
    error.value = e.message || 'Failed to update transaction.'
  } finally {
    loading.value = false
  }
}


const currencies = walletStore.currencies

</script>






<template>
  <form @submit.prevent="handleSubmit" class="update-transaction-form">
    <div>
      <label for="wallet">Wallet:</label>
      <select id="wallet" v-model="form.walletId" required>
        <option v-for="wallet in wallets" :key="wallet.id" :value="wallet.id">
          {{ wallet.name }} ({{ currencies.find(c => c.id == wallet.currency).code }})
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
        step="1"
        v-model.number="form.amount"
        required
        min="0"
      />
    </div>

    <div>
      <label for="comment">Comment:</label>
      <textarea id="comment" v-model="form.comment" placeholder="Optional comment"></textarea>
    </div>

    <button type="submit" @click="router.push('/transactions')" :disabled="loading">Update Transaction</button>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">Transaction updated successfully!</p>
  </form>
  <p>
    <router-link :to="`/transactions/${transactionId}`">Back to Transaction Details</router-link>
  </p>
</template>





