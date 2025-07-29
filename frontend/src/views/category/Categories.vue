<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCategoryStore } from '@/stores/categories'

const router = useRouter()
const categories = useCategoryStore()
const error = ref('')

const categoryList = ref([])

async function loadCategories() {
  try {
    await categories.fetchCategories()
    categoryList.value = categories.categories
    error.value = ''
  } catch (e) {
    error.value = 'Failed to load categories.'
    console.error(e)
  }
}

async function handleDeleteCategory(id) {
  try {
    await categories.deleteCategory(id)
    await loadCategories()
  } catch (e) {
    error.value = 'Failed to delete category. Please try again.'
    console.error(e)
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <div class="categories-container">
    <h1>Categories</h1>
    <div v-if="categoryList.length" class="categories-list grid-4-cols">
      <div v-for="category in categoryList" :key="category.id" class="category-item">
        <h2>{{ category.name }}</h2>
        <p>Type: {{ category.is_income ? 'Income' : 'Expense' }}</p>
        <button @click="router.push(`/categories/edit/${category.id}`)">Edit</button>
        <button @click="handleDeleteCategory(category.id)">Delete</button>
      </div>
    </div>
    <p v-else>No categories found.</p>
    <button @click="router.push('/categories/add')">Add New Category</button>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<style scoped>
.grid-4-cols {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.category-item {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.categories-container {
  max-width: 600px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #ddd;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.categories-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.category-item h2 {
  margin: 0 0 6px 0;
}

.category-item p {
  margin: 0;
  font-weight: 600;
}

.category-item button {
  width: 80px;
  margin-top: 8px;
  padding: 6px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.category-item button:first-of-type {
  background-color: #1976d2;
  color: white;
  margin-right: 8px;
}

.category-item button:first-of-type:hover {
  background-color: #1565c0;
}

.category-item button:last-of-type {
  background-color: #d32f2f;
  color: white;
}

.category-item button:last-of-type:hover {
  background-color: #b71c1c;
}

button {
  padding: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 700;
  background-color: #1976d2;
  color: white;
  width: 100%;
  max-width: 200px;
  display: block;
  margin: 0 auto;
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
