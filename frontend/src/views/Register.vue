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
  <div class="register-wrapper">
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
        Already have an account?
        <router-link to="/login">Login here</router-link>.
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-wrapper {
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

.register-card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  width: 100%;
  text-align: center;
  border: 1px solid #fca5a5;
}

.register-title {
  font-size: 2rem;
  color: #dc2626;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.register-form {
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

.register-button {
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

.register-button:hover {
  background-color: #b91c1c;
}

.error-msg {
  margin-top: 0.5rem;
  color: #b91c1c;
  font-weight: 600;
  text-align: center;
}

.login-msg {
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #7f1d1d;
  text-align: center;
}

.login-msg a {
  color: #dc2626;
  text-decoration: underline;
  font-weight: 500;
}
</style>
