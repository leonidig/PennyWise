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
        router.push('/home')
    } catch (err) {
        error.value = err.message
    }
}

</script>

<template>
    <div class="login-container">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="text" id="email" v-model="email" required>
        </div>
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit">Login</button>
        </form>
        <p v-if="error" style="color: red;">{{ error }}</p>
        <p>Don't have an account? <router-link to="/register">Register here</router-link>.</p>
    </div>
</template>
