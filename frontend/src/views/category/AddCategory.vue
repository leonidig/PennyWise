<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCategoryStore } from '@/stores/categories'

const router = useRouter()
const categories = useCategoryStore()

const error = ref('')
const categoryName = ref('')
const isIncome = ref(false)

async function handleAddCategory() {
    console.log('Incomeadd', isIncome.value)
    try {
        await categories.addCategory(
            categoryName.value,
            isIncome.value,
        );
        
        router.push('/categories');
    } catch (err) {
        console.error('Error adding category:', err);
        error.value = 'Failed to add category. Please try again.';
    }
}


</script>

<template>
  <div class="add-category-container">
    <h1>Add Category</h1>
    <form @submit.prevent="handleAddCategory">
      <div class="form-group">
        <label for="name">Category Name:</label>
        <input type="text" id="name" v-model="categoryName" required>
      </div>
      <div class="form-group">
        <label for="isIncome">Is Income:</label>
        <input type="checkbox" id="isIncome" v-model="isIncome">
      </div>
      <button type="submit">Add Category</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
    <p>Go back to <router-link to="/categories">Categories</router-link>.</p>
  </div>
</template>