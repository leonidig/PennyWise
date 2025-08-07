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

onMounted(loadCategories)
</script>

<template>
  <div class="categories-container">
    <div v-if="categoryList.length" class="grid-4-cols">
      <div v-for="category in categoryList" :key="category.id" class="category-card">
        <h2>{{ category.name }}</h2>
        <p class="type-label" :class="category.is_income ? 'income' : 'expense'">
          {{ category.is_income ? 'Income' : 'Expense' }}
        </p>
        <div class="actions">
          <button @click="router.push(`/categories/edit/${category.id}`)" class="btn-edit">Edit</button>
          <button @click="handleDeleteCategory(category.id)" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>

    <p v-else class="no-categories">No categories found.</p>

    <div class="add-btn-wrapper">
      <button @click="router.push('/categories/add')" class="btn-add">+ Add New Category</button>
    </div>

    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<style scoped>
.categories-container {
  max-width: 1200px;
  margin: 3rem auto;
  padding: 0 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


.grid-4-cols {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
}

.category-card {
  background: #fff;
  border-radius: 20px;
  padding: 3.5rem 2.5rem 3rem;
  box-shadow: 0 10px 25px rgba(220, 38, 38, 0.2);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 260px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: default;
}

.category-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 18px 40px rgba(220, 38, 38, 0.3);
}

.category-card h2 {
  margin: 0 0 1.5rem 0;
  font-size: 2.2rem;
  color: #b91c1c;
  font-weight: 900;
}

.type-label {
  font-weight: 800;
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  user-select: none;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.income {
  color: #15803d;
}

.expense {
  color: #dc2626;
}


.actions {
  margin-top: auto;
  display: flex;
  gap: 12px;
  justify-content: flex-start;
}

.actions button {
  padding: 0.7rem 1.2rem;
  border-radius: 12px;
  border: none;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  color: white;
  transition: background-color 0.3s ease, box-shadow 0.25s ease;
  user-select: none;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
  min-width: 90px;
  text-align: center;
}

.actions button:focus-visible {
  outline: 3px solid #fca5a5;
  outline-offset: 2px;
}

.btn-edit {
  background-color: #2563eb;
  box-shadow: 0 5px 15px rgba(37, 99, 235, 0.5);
}

.btn-edit:hover {
  background-color: #1e40af;
  box-shadow: 0 8px 22px rgba(30, 64, 175, 0.75);
}

.btn-delete {
  background-color: #dc2626;
  box-shadow: 0 5px 15px rgba(220, 38, 38, 0.5);
}

.btn-delete:hover {
  background-color: #991b1b;
  box-shadow: 0 8px 22px rgba(153, 27, 27, 0.75);
}

.btn-add {
  display: block;
  max-width: 320px;
  margin: 4rem auto 0 auto;
  padding: 1.4rem 3rem;
  background-color: #dc2626;
  color: white;
  font-weight: 900;
  font-size: 1.5rem;
  border: none;
  border-radius: 22px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  text-align: center;
  user-select: none;
  box-shadow: 0 8px 30px rgba(220, 38, 38, 0.55);
}

.btn-add:hover {
  background-color: #991b1b;
  box-shadow: 0 12px 40px rgba(153, 27, 27, 0.8);
}

.no-categories {
  text-align: center;
  color: #7f1d1d;
  font-weight: 700;
  margin-top: 5rem;
  font-size: 1.5rem;
}

.error-message {
  margin-top: 3rem;
  text-align: center;
  color: #b91c1c;
  font-weight: 900;
  font-size: 1.25rem;
}

.add-btn-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 4rem;
}


</style>
