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
  <div class="edit-wrapper">
    <div class="edit-card">
      <h1 class="edit-title">Edit Category</h1>

      <form @submit.prevent="handleEditCategory" class="edit-form">
        <div class="form-group">
          <label for="name">Category Name</label>
          <input type="text" id="name" v-model="newCategoryName" />
        </div>

        <div class="form-group checkbox-group">
          <input type="checkbox" id="isIncome" v-model="newIsIncome" />
          <label for="isIncome">Income Category</label>
        </div>

        <button type="submit">Save Changes</button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
      <p class="back-link">
        ← <router-link to="/categories">Back to Categories</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.edit-wrapper {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 500px;
  padding: 2rem;
  box-sizing: border-box;
  background: linear-gradient(135deg, #fff5f5, #ffe4e6);
  z-index: 1000;
}

.edit-card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 3rem 2.5rem;
  width: 100%;
  text-align: center;
  border: 1px solid #fca5a5;
  box-sizing: border-box;
  font-family: 'Segoe UI', sans-serif;
}

.edit-title {
  font-size: 2rem;
  color: #dc2626;
  margin-bottom: 2rem;
  font-weight: 700;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #7f1d1d;
}

input[type="text"] {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff8f8;
  transition: border-color 0.2s ease;
}

input[type="text"]:focus {
  outline: none;
  border-color: #dc2626;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

input[type="checkbox"] {
  transform: scale(1.2);
  accent-color: #dc2626;
}

button[type="submit"] {
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: white;
  background-color: #dc2626;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  width: 100%;
}

button[type="submit"]:hover {
  background-color: #991b1b;
  box-shadow: 0 10px 30px rgba(153, 27, 27, 0.5);
}

.error {
  color: #dc2626;
  text-align: center;
  margin-top: 1rem;
  font-weight: 600;
}

.back-link {
  text-align: center;
  margin-top: 2rem;
  font-weight: 500;
}

.back-link a {
  color: #991b1b;
  text-decoration: underline;
}
</style>