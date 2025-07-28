<script setup>
import { onMounted, ref, computed } from 'vue'
import { useWalletStore } from '@/stores/wallets'
import { useRoute, useRouter } from 'vue-router'

const wallets = useWalletStore()



onMounted(async () => {
  wallets.fetchWallets()
  wallets.fetchCurrencies()
})



const route = useRoute()
const router = useRouter()

const wallet = computed(() =>
  wallets.balances.find(w => w.id == route.params.id)
)

console.log('Editing wallet:', wallet.value)

const currencies = computed(() =>
  wallets.currencies
)

const newName = ref('')
const newCurrency = ref(null)

const updateWallet = async () => {
  if (newName.value && newCurrency.value) {
    await wallets.updateWallet(wallet.value.id,
      newName.value,
      newCurrency.value,
      wallet.value.balance,
    )

    router.push(`/wallets/${wallet.value.id}`)
  } else {
    alert('Please fill in all fields.')
  }
}

</script>


<template>
  <div class="edit-wallet-container">
    <h1>Edit Wallet</h1>
    <form @submit.prevent="updateWallet">
      <div class="form-group">
        <label for="name">Wallet Name:</label>
        <input type="text" id="name" v-model="newName" :placeholder="wallet.name" required>
      </div>
      <div class="form-group">
        <label for="currency">Currency:</label>
        <select id="currency" v-model="newCurrency" required>
          <option v-for="currency in currencies" :key="currency.id" :value="currency.id">{{ currency.code }}</option>
        </select>
      </div>
      <button type="submit">Update Wallet</button>
    </form>
    <p>Go back to <router-link :to="`/wallets/${wallet.id}`">Wallet Details</router-link>.</p>
  </div>
</template>
