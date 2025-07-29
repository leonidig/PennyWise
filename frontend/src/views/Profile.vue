<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
onMounted(async () => {
  await auth.fetchUser()
})

// const passwordVisible = ref(false)
</script>

<template>
  <div class="profile-container">
    <div class="profile-card">
      <h1 class="profile-title">Profile</h1>

      <div class="profile-info">
        <p><strong>Email:</strong> {{ auth.email || 'Loading...' }}</p>

        <!--
        <p v-if="passwordVisible"><strong>Password:</strong> {{ auth.password }}</p>
        <p v-else><strong>Password:</strong> ********</p>
        <button class="toggle-password-btn" @click="passwordVisible = !passwordVisible">
          {{ passwordVisible ? 'Hide Password' : 'Show Password' }}
        </button>
        -->
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fef2f2;
  padding: 1rem;
}

.profile-card {
  background-color: #fff;
  border: 2px solid #f87171;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 10px rgba(220, 38, 38, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.profile-title {
  color: #dc2626;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
}

.profile-info p {
  font-size: 1.1rem;
  color: #7f1d1d;
  margin: 0.75rem 0;
}

.toggle-password-btn {
  margin-top: 1rem;
  background-color: #dc2626;
  border: none;
  border-radius: 8px;
  color: white;
  padding: 0.5rem 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.toggle-password-btn:hover {
  background-color: #b91c1c;
}
</style>
