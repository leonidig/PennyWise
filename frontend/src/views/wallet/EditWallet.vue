<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useWalletStore } from '@/stores/wallets'
import { useRoute, useRouter } from 'vue-router'

const wallets = useWalletStore()
const route = useRoute()
const router = useRouter()

const loading = ref(true)

onMounted(async () => {
  await wallets.fetchWallets()
  await wallets.fetchCurrencies()
  loading.value = false
})

// Reactive computed wallet based on route param
const wallet = computed(() =>
  wallets.balances.find(w => w.id == route.params.id)
)

const currencies = computed(() => wallets.currencies)

const newName = ref('')
const newCurrency = ref(null)

// Initialize form fields when wallet is ready
watch(
  () => wallet.value,
  (w) => {
    if (w) {
      newName.value = w.name
      newCurrency.value = w.currency
    }
  },
  { immediate: true }
)

const updateWallet = async () => {
  if (!newName.value || !newCurrency.value) {
    alert('Please fill in all fields.')
    return
  }

  try {
    await wallets.updateWallet(
      wallet.value.id,
      newName.value,
      newCurrency.value,
      wallet.value.balance
    )
    router.push(`/wallets/${wallet.value.id}`)
  } catch (error) {
    alert('Failed to update wallet. Please try again.')
    console.error(error)
  }
}
</script>

<template>
  <div class="edit-wallet-container" v-if="!loading && wallet">
    <h1>Edit Wallet</h1>
    <form @submit.prevent="updateWallet" class="form">
      <div class="form-group">
        <label for="name">Wallet Name:</label>
        <input
          type="text"
          id="name"
          v-model="newName"
          required
          placeholder="Wallet name"
        />
      </div>

      <div class="form-group">
        <label for="currency">Currency:</label>
        <select id="currency" v-model="newCurrency" required>
          <option value="" disabled>Select a currency</option>
          <option v-for="currency in currencies" :key="currency.id" :value="currency.id">
            {{ currency.code }}
          </option>
        </select>
      </div>

      <button type="submit" class="btn btn-primary">Update Wallet</button>
    </form>
    <p>
      Go back to
      <router-link :to="`/wallets/${wallet.id}`">Wallet Details</router-link>.
    </p>
  </div>

  <div v-else>
    <p>Loading wallet data...</p>
  </div>
</template>

<style scoped>
.edit-wallet-container {
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
