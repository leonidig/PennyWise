<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import {useWalletStore} from '@/stores/wallets';
import { useRouter } from 'vue-router';


const wallets = useWalletStore();

const router = useRouter();
const walletName = ref('');
const selectedCurrency = ref('');
const initialBalance = ref(0);
wallets.fetchCurrencies();
const currencies = wallets.currencies;

async function addWallet() {
    try {
        await wallets.addWallet(
            walletName.value,
            parseFloat(initialBalance.value),
            selectedCurrency.value,

        );

        router.push('/wallets');
    } catch (error) {
        console.error('Error adding wallet:', error);
        alert('Failed to add wallet. Please try again.');
    }
}

</script>

<template>
  <div class="add-wallet-container">
    <h1>Add Wallet</h1>
    <form @submit.prevent="addWallet">
      <div class="form-group">
        <label for="name">Wallet Name:</label>
        <input type="text" id="name" v-model="walletName" required>
      </div>
      <div class="form-group">
        <label for="currency">Currency:</label>
        <select id="currency" v-model="selectedCurrency" required>
          <option v-for="currency in currencies" :key="currency" :value="currency['id']">{{ currency.code }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="balance">Initial Balance:</label>
        <input type="number" id="balance" v-model.number="initialBalance" required>
      </div>
      <button type="submit">Add Wallet</button>
    </form>
  </div>
</template>
