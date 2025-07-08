import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: "/home",
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta : {
            requiresAuth: true
        }
    },

    {
        path: "/login",
        name: "Login",
        component: () => import('@/views/Login.vue'),
    },

    {
        path: "/register",
        name: "Register",
        component: () => import('@/views/Login.vue'),
    },
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