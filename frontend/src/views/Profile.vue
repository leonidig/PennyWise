<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'


const auth = useAuthStore()
onMounted(async() => {
  await auth.fetchUser()
})
// const passwordVisible = ref(false)

</script>

<template>
  <div class="profile-container">
    <h1>Profile</h1>
    <p>Email: {{ auth.email }}</p>
    <!-- <p v-if="passwordVisible">Password: {{ auth.password }}</p>
    <p v-else>Password: ********</p>
    <button @click="passwordVisible = !passwordVisible">
      {{ passwordVisible ? 'Hide Password' : 'Show Password' }} -->
    <!-- </button> -->
  </div>
</template>
