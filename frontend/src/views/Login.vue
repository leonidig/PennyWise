<template>
  <div class="login-wrapper">
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
        Don't have an account?
        <router-link to="/register">Register here</router-link>.
      </p>
    </div>
  </div>
</template>

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

<style scoped>
.login-wrapper {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  box-sizing: border-box;
  background: linear-gradient(135deg, #fff5f5, #ffe4e6);
  z-index: 10;
}

.login-card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  width: 100%;
  text-align: center;
  border: 1px solid #fca5a5;
}

.login-title {
  font-size: 2rem;
  color: #dc2626;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  color: #7f1d1d;
  font-weight: 600;
  font-size: 0.95rem;
}

input {
  padding: 0.65rem 0.85rem;
  border: 1px solid #fca5a5;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.15);
}

.login-button {
  padding: 0.75rem;
  background-color: #dc2626;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-button:hover {
  background-color: #b91c1c;
}

.error-msg {
  margin-top: 0.5rem;
  color: #b91c1c;
  font-weight: 600;
  text-align: center;
}

.register-msg {
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #7f1d1d;
}

.register-msg a {
  color: #dc2626;
  text-decoration: underline;
  font-weight: 500;
}
</style>
