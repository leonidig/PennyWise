<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCategoryStore } from '@/stores/categories';

const router = useRouter()
const categories = useCategoryStore()

const error = ref('')
const categoryList = categories.categories
</script>

<template>
  <div class="categories-container">
    <h1>Categories</h1>
    <div class="categories-list">
      <div v-for="category in categoryList" :key="category.id" class="category-item">
        <h2>{{ category.name }}</h2>
        <p>Type: {{ category.is_income ? 'Income' : 'Expense' }}</p>
        <button @click="router.push(`/categories/edit/${category.id}`)">Edit</button>
      </div>
    </div>
    <button @click="router.push('/categories/add')">Add New Category</button>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>