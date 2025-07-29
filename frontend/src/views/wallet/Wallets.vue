<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWalletStore } from '@/stores/wallets'

const wallets = useWalletStore()
const router = useRouter()

const deletingWalletIds = ref(new Set())
const loading = ref(true)

onMounted(async () => {
  try {
    await wallets.fetchWallets()
    await wallets.fetchCurrencies()
  } finally {
    loading.value = false
  }
})

const confirmAndDeleteWallet = async (id, name) => {
  if (confirm(`Are you sure you want to delete wallet "${name}"? This action cannot be undone.`)) {
    deletingWalletIds.value.add(id)
    try {
      await wallets.deleteWallet(id)
    } catch (error) {
      alert('Failed to delete wallet.')
      console.error(error)
    } finally {
      deletingWalletIds.value.delete(id)
    }
  }
}
</script>

<template>
  <div class="wallets-container">
    <h1>Wallets</h1>

    <div v-if="loading">Loading wallets...</div>

    <div v-else class="wallets-list grid-4-cols">
      <div v-if="wallets.balances.length === 0">No wallets found. Add one!</div>

      <div
        v-for="wallet in wallets.balances"
        :key="wallet.id"
        class="wallet-item"
      >
        <h2>{{ wallet.name }}</h2>
        <p>
          Balance: {{ wallet.balance }}
          {{
            wallets.currencies.find(c => c.id === wallet.currency)?.code ||
            'N/A'
          }}
        </p>
        <button @click="router.push(`/wallets/${wallet.id}`)" :disabled="deletingWalletIds.has(wallet.id)">
          View Details
        </button>
        <button @click="router.push(`/wallets/edit/${wallet.id}`)" :disabled="deletingWalletIds.has(wallet.id)">
          Edit
        </button>
        <button
          @click="confirmAndDeleteWallet(wallet.id, wallet.name)"
          :disabled="deletingWalletIds.has(wallet.id)"
        >
          {{ deletingWalletIds.has(wallet.id) ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </div>

    <button @click="router.push('/wallets/add')">Add New Wallet</button>
  </div>
</template>

<style scoped>
.grid-4-cols {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.wallet-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.wallets-container {
  padding: 1rem;
  width: 1000px;
}

.wallets-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  padding: 0.5rem;
  width: 100%;
  box-sizing: border-box;
}




.wallet-item h2 {
  margin: 0 0 0.25rem 0;
}

.wallet-item p {
  margin: 0 0 0.75rem 0;
}

button {
  margin-right: 0.5rem;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
