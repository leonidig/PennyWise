<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const error = ref('')
const email = ref('')
const password = ref('')

async function handleLogin() {
  error.value = ''
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">Login</h1>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="text" id="email" v-model="email" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <button type="submit" class="login-button">Login</button>

        <p v-if="error" class="error-msg">{{ error }}</p>
      </form>

      <p class="register-msg">
        Don't have an account? <router-link to="/register">Register here</router-link>.
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fef2f2;
  padding: 1rem;
}

.login-card {
  background-color: #ffffff;
  border: 2px solid #f87171;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(220, 38, 38, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-title {
  color: #dc2626;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.25rem;
  color: #7f1d1d;
  font-weight: 500;
}

input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #f87171;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #dc2626;
  box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1);
}

.login-button {
  padding: 0.75rem;
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #b91c1c;
}

.error-msg {
  margin-top: 0.5rem;
  color: #dc2626;
  font-weight: 500;
}

.register-msg {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #7f1d1d;
}

.register-msg a {
  color: #dc2626;
  text-decoration: underline;
}
</style>
