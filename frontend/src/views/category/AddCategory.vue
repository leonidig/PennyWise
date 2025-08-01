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
  <div class="page-wrapper">
    <div class="add-category-wrapper">
      <h1 class="title">Add Category</h1>
      <form @submit.prevent="handleAddCategory" class="form">
        <div class="form-group">
          <label for="name">Category Name:</label>
          <input
            type="text"
            id="name"
            v-model="categoryName"
            required
            autocomplete="off"
            placeholder="Enter category name"
          />
        </div>

        <div class="form-group toggle-group">
          <input type="checkbox" id="isIncome" v-model="isIncome" />
          <label for="isIncome" class="toggle-label">
            <span class="toggle-slider"></span>
            Is Income
          </label>
        </div>

        <button type="submit" class="submit-btn">Add Category</button>
      </form>

      <p v-if="error" class="error-message">{{ error }}</p>

      <p class="back-link">
        Go back to <router-link to="/categories">Categories</router-link>.
      </p>
    </div>
  </div>
</template>

<style scoped>

.page-wrapper {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff5f5;
  padding: 3rem 2rem;
  border-radius: 20px;
  box-shadow:
    0 4px 25px rgba(220, 38, 38, 0.2),
    inset 0 0 20px rgba(255, 215, 215, 0.35);
  max-width: 440px;
  width: 90vw;
  font-family: 'Inter', Arial, sans-serif;
  color: #7f1d1d;
  user-select: none;
  text-align: center;
}

.title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #dc2626;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px #f87171aa;
}


.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  text-align: left;
}

.form-group {
  position: relative;
}


label {
  display: block;
  margin-bottom: 0.6rem;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  user-select: none;
}


input[type='text'] {
  width: 100%;
  padding: 0.85rem 1rem;
  font-size: 1rem;
  border-radius: 12px;
  border: 2px solid #f87171;
  background: #fff0f0;
  color: #7f1d1d;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  outline-offset: 2px;
}

input[type='text']::placeholder {
  color: #fca5a5;
  font-weight: 400;
}

input[type='text']:focus {
  border-color: #dc2626;
  box-shadow:
    0 0 10px 3px rgba(220, 38, 38, 0.35);
  background: #fff5f5;
}


.toggle-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  user-select: none;
  position: relative;
}

.toggle-group input[type='checkbox'] {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.toggle-label {
  position: relative;
  padding-left: 52px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  color: #7f1d1d;
  display: inline-block;
  vertical-align: middle;
  user-select: none;
}


.toggle-slider {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  width: 46px;
  height: 26px;
  background: #f87171;
  border-radius: 9999px;
  box-shadow: inset 0 0 9px rgba(255, 255, 255, 0.6);
  transition: background-color 0.3s ease;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  top: 2.5px;
  left: 2.5px;
  width: 21px;
  height: 21px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 6px rgba(0,0,0,0.18);
  transition: transform 0.3s ease;
}

.toggle-group input[type='checkbox']:checked + .toggle-label .toggle-slider {
  background: #dc2626;
}

.toggle-group input[type='checkbox']:checked + .toggle-label .toggle-slider::before {
  transform: translateX(20px);
}


.submit-btn {
  width: 100%;
  padding: 14px 0;
  background: linear-gradient(135deg, #dc2626, #f87171);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 1.15rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow:
    0 6px 12px rgba(220, 38, 38, 0.5);
  transition: background 0.3s ease, box-shadow 0.3s ease;
  user-select: none;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #b91c1c, #f43f3f);
  box-shadow:
    0 8px 20px rgba(220, 38, 38, 0.7);
}


.error-message {
  margin-top: 1rem;
  font-weight: 700;
  text-align: center;
  color: #b91c1c;
  user-select: none;
}


.back-link {
  margin-top: 2rem;
  font-weight: 600;
  text-align: center;
}

.back-link a {
  color: #dc2626;
  text-decoration: underline;
  font-weight: 700;
  cursor: pointer;
  user-select: none;
}

.back-link a:hover {
  color: #b91c1c;
}
</style>
