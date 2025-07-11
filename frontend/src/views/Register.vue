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
    <h1>Register</h1>
    <form @submit.prevent="handleRegister">
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="text" id="email" v-model="email" required>
        </div>
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>
        </div>
        <div class="form-group">
            <label for="confirm-password">Confirm Password:</label>
            <input type="password" id="confirm-password" v-model="confirmPassword" required>
        </div>
        <button type="submit">Register</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
    <p>Already have an account? <router-link to="/login">Login here</router-link>.</p>
</div>

</template>