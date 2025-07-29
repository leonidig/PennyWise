<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')

async function handleRegister() {
  error.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  try {
    await auth.register(email.value, password.value, confirmPassword.value)
    router.push('/login')
  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <h1 class="register-title">Register</h1>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="text" id="email" v-model="email" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <div class="form-group">
          <label for="confirm-password">Confirm Password</label>
          <input type="password" id="confirm-password" v-model="confirmPassword" required />
        </div>

        <button type="submit" class="register-button">Register</button>

        <p v-if="error" class="error-msg">{{ error }}</p>
      </form>

      <p class="login-msg">
        Already have an account? <router-link to="/login">Login here</router-link>.
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fef2f2;
  padding: 1rem;
}

.register-card {
  background-color: #ffffff;
  border: 2px solid #f87171;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(220, 38, 38, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.register-title {
  color: #dc2626;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
}

.register-form {
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

.register-button {
  padding: 0.75rem;
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-button:hover {
  background-color: #b91c1c;
}

.error-msg {
  margin-top: 0.5rem;
  color: #dc2626;
  font-weight: 500;
}

.login-msg {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #7f1d1d;
}

.login-msg a {
  color: #dc2626;
  text-decoration: underline;
}
</style>
