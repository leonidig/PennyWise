<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCategoryStore } from '@/stores/categories'

const router = useRouter()
const categoriesStore = useCategoryStore()
const categoryList = categoriesStore.categories
const error = ref('')
const newCategoryName = ref('')
const newIsIncome = ref(false)
const categoryId = ref(null)

categoryId.value = router.currentRoute.value.params.id

const category = categoriesStore.getCategoryById(categoryId.value)


async function handleEditCategory() {
    try {
        await categoriesStore.updateCategory(newCategoryName.value, newIsIncome.value, categoryId.value);
        router.push('/categories');
    } catch (err) {
        console.error('Error updating category:', err);
        error.value = 'Failed to update category. Please try again.';
    }
}



</script>

<template>
  <div class="edit-category-container">
    <h1>Edit Category</h1>
    <form @submit.prevent="handleEditCategory">
      <div class="form-group">
        <label for="name" placeholder="{{ category.name }}">Category Name:</label>
        <input type="text" id="name" v-model="newCategoryName" required>
      </div>
      <div class="form-group">
        <label for="isIncome">Is Income:</label>
        <input type="checkbox" id="isIncome" v-model="newIsIncome" :checked="category.is_income">
      </div>
      <button type="submit">Update Category</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
    <p>Go back to <router-link to="/categories">Categories</router-link>.</p>
  </div>

</template>