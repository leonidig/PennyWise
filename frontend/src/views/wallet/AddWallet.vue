<script setup>
import { ref, onMounted } from 'vue'
import { useWalletStore } from '@/stores/wallets'
import { useRouter } from 'vue-router'

const wallets = useWalletStore()
const router = useRouter()

const walletName = ref('')
const selectedCurrency = ref('')
const initialBalance = ref(0)

const currencies = ref([])

onMounted(async () => {
  await wallets.fetchCurrencies()
  currencies.value = wallets.currencies
})

async function addWallet() {
  try {
    await wallets.addWallet(
      walletName.value,
      parseFloat(initialBalance.value),
      selectedCurrency.value
    )
    router.push('/wallets')
  } catch (error) {
    console.error('Error adding wallet:', error)
    alert('Failed to add wallet. Please try again.')
  }
}
</script>

<template>
  <div class="add-wallet-container">
    <h1>Add Wallet</h1>
    <form @submit.prevent="addWallet" class="form">
      <div class="form-group">
        <label for="name">Wallet Name:</label>
        <input
          type="text"
          id="name"
          v-model="walletName"
          required
          placeholder="Enter wallet name"
        />
      </div>

      <div class="form-group">
        <label for="currency">Currency:</label>
        <select id="currency" v-model="selectedCurrency" required>
          <option value="" disabled>Select a currency</option>
          <option
            v-for="currency in currencies"
            :key="currency.id"
            :value="currency.id"
          >
            {{ currency.code }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="balance">Initial Balance:</label>
        <input
          type="number"
          id="balance"
          v-model.number="initialBalance"
          step="0.01"
          min="0"
          required
          placeholder="0.00"
        />
      </div>

      <button type="submit" class="btn btn-primary">Add Wallet</button>
    </form>
  </div>
</template>

<style scoped>
.add-wallet-container {
  padding: 1rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
}

input,
select {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #2563eb;
}
</style>
