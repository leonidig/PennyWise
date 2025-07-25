<template>
  <nav class="avbar navbar-expand-lg navbar-light bg-dark">
    <div class="navbar-brand">
      <router-link to="/" class="brand-link">PennyWise</router-link>
      <button class="toggle-btn" @click="isOpen = !isOpen" aria-label="Toggle menu">
        ☰
      </button>
    </div>

    <div :class="['nav-collapse', { open: isOpen }]">
      <ul class="nav-list">
        <li><router-link to="/" class="nav-link" @click="closeMenu">Home</router-link></li>
      </ul>

      <ul class="nav-list right">
        <li class="dropdown" @mouseleave="isDropdownOpen = false">
          <button class="dropdown-btn" @click="isDropdownOpen = !isDropdownOpen">
            User ▾
          </button>
          <ul v-if="isDropdownOpen" class="dropdown-menu">
            <li><router-link to="/profile" class="dropdown-item" @click="closeMenu">Profile</router-link></li>
            <li><a href="#" @click.prevent="signOut">Sign Out</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const isOpen = ref(false)
const isDropdownOpen = ref(false)

function closeMenu() {
  isOpen.value = false
  isDropdownOpen.value = false
}

function signOut() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background-color: #006315f2;
  color: white;
  padding: 0.5rem 1rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  font-weight: bold;
  color: white;
  text-decoration: none;
  font-size: 1.25rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  margin-left: 1rem;
  display: none;
}

.nav-collapse {
  display: flex;
  flex-grow: 1;
  justify-content: space-between;
  align-items: center;
}

.nav-list {
  list-style: none;
  padding-left: 0;
  margin: 0;
  display: flex;
  align-items: center;
}

.nav-list.right {
  margin-left: auto;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
}

.nav-link:hover {
  text-decoration: underline;
}

.dropdown {
  position: relative;
}

.dropdown-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  background: white;
  color: black;
  min-width: 150px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  border-radius: 4px;
  margin-top: 0.5rem;
  z-index: 1000;
}

.dropdown-item {
  display: block;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: black;
}

.dropdown-item:hover {
  background-color: #eee;
}

/* Responsive: show toggle button and hide nav links on small screens */
@media (max-width: 768px) {
  .toggle-btn {
    display: inline-block;
  }
  .nav-collapse {
    width: 100%;
    flex-direction: column;
    display: none;
  }
  .nav-collapse.open {
    display: flex;
  }
  .nav-list {
    flex-direction: column;
    width: 100%;
  }
  .nav-link, .dropdown-btn {
    padding: 1rem;
    width: 100%;
  }
  .dropdown-menu {
    position: static;
    box-shadow: none;
    background: #424242ff;
    margin: 0;
  }
}
</style>
