<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="brand-link">PennyWise</router-link>
      <button
        class="toggle-btn"
        @click="isOpen = !isOpen"
        aria-label="Toggle menu"
      >
        ☰
      </button>
    </div>

    <div :class="['nav-collapse', { open: isOpen }]">
      <ul class="nav-list main-links">
        <li><router-link to="/wallets" @click="closeMenu">Wallets</router-link></li>
      </ul>
      <ul class="nav-list main-links">
        <li><router-link to="/transactions" @click="closeMenu">Transactions</router-link></li>
      </ul>
      <ul class="nav-list main-links">
        <li><router-link to="/categories" @click="closeMenu">Categories</router-link></li>
      </ul>

      <ul class="nav-list user-links">
        <li class="dropdown">
          <button class="dropdown-btn" @click="isDropdownOpen = !isDropdownOpen">
            {{ auth.email }} ▾
          </button>
          <ul v-if="isDropdownOpen" class="dropdown-menu">
            <li><router-link to="/profile" @click="closeMenu">Profile</router-link></li>
            <li><a href="#" @click.prevent="signOut">Sign Out</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth'
import router from '@/router';



const auth = useAuthStore()

onMounted(async() => {
  await auth.fetchUser();
});


const isOpen = ref(false);
const isDropdownOpen = ref(false);






function closeMenu() {
  isOpen.value = false;
  isDropdownOpen.value = false;
}

function signOut() {
  alert('Signed out');
  auth.logout();
  router.push('/login');

}
</script>

<style>
.navbar {
  display: flex;
  justify-content: space-between; /* or flex-start */
  align-items: center;
  padding: 1rem;
  width: 100%;
  background-color: #000000; /* dark green */
  color: white;
  position: fixed;
  top: 0;
  left: 0;
}



.navbar-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-link {
  color: white;
  font-weight: bold;
  text-decoration: none;
  font-size: 1.25rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  display: none; /* hide on desktop */
}

.nav-collapse {
  display: flex;
  flex-grow: 1;
  justify-content: flex-start;
  align-items: center;
  gap: 1rem;
}

.nav-list {
  list-style: none;
  display: flex;
  margin: 0;
  padding: 0;
}

.nav-list.main-links {
  gap: 1rem;
}

.nav-list.user-links {
  margin-left: auto;
  gap: 1rem;
}

.nav-list li a,
.dropdown-btn {
  color: white;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.nav-list li a:hover,
.dropdown-btn:hover {
  text-decoration: underline;
}

.dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  color: black;
  min-width: 150px;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  z-index: 100;
}

.dropdown-menu li {
  padding: 0.5rem 1rem;
}

.dropdown-menu li a {
  color: black;
  text-decoration: none;
  display: block;
}

.dropdown-menu li a:hover {
  background-color: #eee;
}

/* Responsive: show toggle button on small screens and stack menu vertically */
@media (max-width: 600px) {
  .toggle-btn {
    display: inline-block;
  }
  .nav-collapse {
    flex-direction: column;
    display: none;
    width: 100%;
  }
  .nav-collapse.open {
    display: flex;
  }
  .nav-list {
    flex-direction: column;
    gap: 0;
  }
  .nav-list li {
    padding: 0.5rem 0;
  }
  .nav-list.user-links {
    margin-left: 0;
  }
  .dropdown-menu {
    position: static;
    box-shadow: none;
    border-radius: 0;
    background: #444;
    color: white;
  }
  .dropdown-menu li a {
    color: white;
  }
  .dropdown-menu li a:hover {
    background-color: #555;
  }
}
</style>
