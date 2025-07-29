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
  try {
    await categories.addCategory(categoryName.value.trim(), isIncome.value)
    router.push('/categories')
  } catch (err) {
    console.error('Error adding category:', err)
    error.value = 'Failed to add category. Please try again.'
  }
}
</script>

<template>
  <div class="add-category-container">
    <h1>Add Category</h1>
    <form @submit.prevent="handleAddCategory" class="form">
      <div class="form-group">
        <label for="name">Category Name:</label>
        <input type="text" id="name" v-model="categoryName" required autocomplete="off" />
      </div>
      <div class="form-group checkbox-group">
        <input type="checkbox" id="isIncome" v-model="isIncome" />
        <label for="isIncome">Is Income</label>
      </div>
      <button type="submit">Add Category</button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
    <p>
      Go back to <router-link to="/categories">Categories</router-link>.
    </p>
  </div>
</template>

<style scoped>
.add-category-container {
  font-family: Arial, sans-serif;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fafafa;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

.form-group input[type="text"] {
  width: 100%;
  padding: 8px 10px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-group input[type="checkbox"] {
  margin-right: 8px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

button {
  width: 100%;
  padding: 10px;
  font-weight: 700;
  font-size: 1rem;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #1565c0;
}

.error-message {
  color: red;
  margin-top: 10px;
  font-weight: 600;
  text-align: center;
}
</style>
