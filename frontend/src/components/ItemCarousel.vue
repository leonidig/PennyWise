<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useWalletStore } from '@/stores/wallets'

const wallets = useWalletStore()
wallets.fetchCurrencies()
const currencies = wallets.currencies

const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

const currentIndex = ref(0)

function nextItem() {
  if (currentIndex.value < props.items.length - 1) {
    currentIndex.value++
  }
}

function prevItem() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}
</script>

<template>
  <div class="wallet-carousel">
    <RouterLink to="/wallets" class="wallet-link">View All Wallets</RouterLink>

    <div v-if="items.length > 0 && items[currentIndex]" class="wallet-details">
      <p><strong>Name:</strong> {{ items[currentIndex].name }}</p>
      <p><strong>Balance:</strong>
        {{ items[currentIndex].balance }}
        {{ currencies.find(i => i.id === items[currentIndex].currency)?.code || '' }}
      </p>
    </div>

    <div v-else class="wallet-empty">
      No wallets available.
    </div>

    <div class="wallet-controls" v-if="items.length > 0">
      <button @click="prevItem" :disabled="currentIndex === 0" class="nav-btn">
        ◀ Previous
      </button>

      <span class="page-indicator">
        {{ currentIndex + 1 }} / {{ items.length }}
      </span>

      <button @click="nextItem" :disabled="currentIndex === items.length - 1" class="nav-btn">
        Next ▶
      </button>
    </div>
  </div>
</template>

<style>
.wallet-carousel {
  background-color: #FEF2F2;
  border: 2px solid #F87171;
  border-radius: 12px;
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  color: #7F1D1D;
  box-shadow: 0 4px 8px rgba(220, 38, 38, 0.1);
  font-family: 'Segoe UI', sans-serif;
}

.wallet-link {
  display: inline-block;
  color: #DC2626;
  text-decoration: none;
  font-weight: bold;
  margin-bottom: 12px;
}

.wallet-link:hover {
  text-decoration: underline;
}

.wallet-details {
  background: white;
  border: 1px solid #F87171;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  text-align: center;
}

.wallet-empty {
  text-align: center;
  color: #9CA3AF;
  font-style: italic;
  margin-bottom: 16px;
}

.wallet-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-btn {
  background-color: #DC2626;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.nav-btn:disabled {
  background-color: #FECACA;
  cursor: not-allowed;
}

.nav-btn:not(:disabled):hover {
  background-color: #B91C1C;
}

.page-indicator {
  font-size: 0.875rem;
  color: #7F1D1D;
}
</style>
