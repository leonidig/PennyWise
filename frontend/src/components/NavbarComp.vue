<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="brand-link">PennyWise</router-link>
      <button
        class="toggle-btn"
        @click="isOpen = !isOpen"
        :aria-expanded="isOpen.toString()"
        aria-label="Toggle menu"
      >
        ☰
      </button>
    </div>

    <div :class="['nav-collapse', { open: isOpen }]">
      <ul class="nav-list main-links">
        <li><router-link to="/wallets" @click="closeMenu">Wallets</router-link></li>
        <li><router-link to="/transactions" @click="closeMenu">Transactions</router-link></li>
        <li><router-link to="/categories" @click="closeMenu">Categories</router-link></li>
      </ul>

      <ul class="nav-list user-links">
        <li class="dropdown">
          <button class="dropdown-btn" @click="isDropdownOpen = !isDropdownOpen" :disabled="!auth.email">
            <template v-if="auth.email">
              {{ auth.email }} ▾
            </template>
            <template v-else>
              Loading...
            </template>
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
import { useAuthStore } from '@/stores/auth';
import router from '@/router';

const auth = useAuthStore();

onMounted(async () => {
  await auth.fetchUser();
});

const isOpen = ref(false);
const isDropdownOpen = ref(false);

function closeMenu() {
  isOpen.value = false;
  isDropdownOpen.value = false;
}

function signOut() {
  auth.logout();
  router.push('/login');
}
</script>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  width: 100%;
  background-color: #7F1D1D;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-link {
  color: #FEF2F2;
  font-weight: bold;
  text-decoration: none;
  font-size: 1.5rem;
}

.brand-link:hover {
  color: #F87171;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  display: none; /* Hidden on desktop */
}

.nav-collapse {
  display: flex;
  flex-grow: 1;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.nav-list {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.nav-list li a,
.dropdown-btn {
  color: #FEF2F2;
  background: none;
  border: none;
  font-size: 1rem;
  text-decoration: none;
  cursor: pointer;
  font-weight: 500;
}

.nav-list li a:hover,
.dropdown-btn:hover {
  color: #F87171;
}

.dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 110%;
  right: 0;
  background-color: white;
  color: #7F1D1D;
  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  overflow: hidden;
  z-index: 999;
  min-width: 150px;
}

.dropdown-menu li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #7F1D1D;
  text-decoration: none;
}

.dropdown-menu li a:hover {
  background-color: #F87171;
  color: white;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .toggle-btn {
    display: block;
  }

  .nav-collapse {
    flex-direction: column;
    display: none;
    width: 100%;
    background-color: #7F1D1D;
    margin-top: 1rem;
    padding: 0 1rem 1rem;
  }

  .nav-collapse.open {
    display: flex;
  }

  .nav-list {
    flex-direction: column;
    gap: 0.5rem;
  }

  .dropdown-menu {
    position: static;
    box-shadow: none;
    background: #F87171;
    color: white;
  }

  .dropdown-menu li a {
    color: white;
  }

  .dropdown-menu li a:hover {
    background-color: #DC2626;
  }
}
</style>
