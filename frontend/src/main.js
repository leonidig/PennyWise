import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

async function initApp() {
  try {
    const response = await fetch('http://localhost:8000/api/csrf/', {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }

    const app = createApp(App)
    const pinia = createPinia()

    app.use(pinia)

    const { default: router } = await import('@/router')

    app.use(router)

    app.mount('#app')

    const { useAuthStore } = await import('./stores/auth.js')
    const auth = useAuthStore()
    if (auth.refresh) {
      auth.startRefreshLoop()
    }

  } catch (error) {
    console.error('App initialization failed:', error.message)
  }
}

initApp()

