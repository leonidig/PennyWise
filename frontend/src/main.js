import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/auth'


fetch('http://localhost:8000/api/csrf/', {
  method: 'GET',
  credentials: 'include',
}).then(() => {
createApp(App).use(router).mount('#app')
app.use(createPinia())
})

const auth = useAuthStore()
  if (auth.refresh) {
    auth.startRefreshLoop()
  }