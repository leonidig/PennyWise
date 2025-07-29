<script setup>
import { ref, watchEffect, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCategoryStore } from '@/stores/categories'

const router = useRouter()
const route = useRoute()
const categoriesStore = useCategoryStore()

const error = ref('')
const newCategoryName = ref('')
const newIsIncome = ref(false)

const categoryId = Number(route.params.id)
const category = ref(null)


onMounted(() => {
  category.value = categoriesStore.getCategoryById(categoryId)
  if (category.value) {
    newCategoryName.value = category.value.name
    newIsIncome.value = category.value.is_income
  } else {
    error.value = 'Category not found.'
  }
})

async function handleEditCategory() {
  error.value = ''
  if (!newCategoryName.value.trim()) {
    error.value = 'Category name cannot be empty.'
    return
  }

  try {
    await categoriesStore.updateCategory(newCategoryName.value, newIsIncome.value, categoryId)
    router.push('/categories')
  } catch (err) {
    console.error('Error updating category:', err)
    error.value = 'Failed to update category. Please try again.'
  }
}
</script>

<template>
  <div class="edit-category-container">
    <h1>Edit Category</h1>
    <form @submit.prevent="handleEditCategory">
      <div class="form-group">
        <label for="name">Category Name:</label>
        <input type="text" id="name" v-model="newCategoryName" required />
      </div>
      <div class="form-group">
        <label for="isIncome">Is Income:</label>
        <input type="checkbox" id="isIncome" v-model="newIsIncome" />
      </div>
      <button type="submit">Update Category</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
    <p>Go back to <router-link to="/categories">Categories</router-link>.</p>
  </div>
</template>

<style scoped>
.edit-category-container {
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 16px;
}

.form-group {
  margin-bottom: 12px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
}

input[type="text"] {
  width: 100%;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input[type="checkbox"] {
  transform: scale(1.2);
  margin-left: 8px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #1976d2;
  color: white;
  font-weight: 700;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #1565c0;
}

p {
  margin-top: 16px;
  text-align: center;
}
</style>
