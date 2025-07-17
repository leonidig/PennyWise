import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

const routes = [
    { path: "/", name: 'Home', component: Home, meta : {requiresAuth: true} },
    { path: "/login", name: "Login", component: Login },
    { path: "/register", name: "Register", component: Register },
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.access ) {
    return '/login'
  }
})
export default router
