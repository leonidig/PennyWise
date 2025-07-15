<script setup>
import {ref} from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  },
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
  <div class="p-4 broder rounded shadow w-full max-w-md">
    <RouterLink to="/">Accounts</RouterLink>  <!-- Implement Accounts Route -->
    <h1 class="text-2xl font-bold mb-4">Total Balance</h1>
    <div class="mb-4 text center">
      <slot :item="items[currentIndex][name]"></slot>
      <slot :item="items[currentIndex][type]"></slot>
      <slot :item="items[currentIndex][number]"></slot>
      <slot :item="items[currentIndex][balance]"></slot>
    </div>
    <div class="flex justify-between items-center">
      <button @click="prevItem" class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50" :disabled="currentIndex === 0">
        Previous
      </button>
      <span class="text-sm text-gray-600">
        Page {{ currentIndex + 1 }} of {{ items.length }}
      </span>
      <button @click="nextItem" class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50" :disabled="currentIndex === items.length - 1">
        Next
      </button>
    </div>
  </div>
</template>


