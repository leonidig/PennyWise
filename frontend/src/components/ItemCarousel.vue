<script setup>
import { ref } from 'vue'

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
  <div class="p-4 border rounded shadow w-full max-w-md">
    <RouterLink to="/" class="text-blue-600 underline">Wallets</RouterLink>

    <div class="mb-4 text-center">
      <slot :item="items[currentIndex]"></slot>
    </div>

    <div class="flex justify-between items-center">
      <button @click="prevItem" :disabled="currentIndex === 0"
              class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50">
        Previous
      </button>

      <span class="text-sm text-gray-600">
        Page {{ currentIndex + 1 }} of {{ items.length }}
      </span>

      <button @click="nextItem" :disabled="currentIndex === items.length - 1"
              class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50">
        Next
      </button>
    </div>
  </div>
</template>
