import { defineStore } from 'pinia'
import { getCSRFToken } from '../utils/csrf'



export const useAuthStore = defineStore('auth', {
    state: () => ({
        access: localStorage.getItem('access') || null,
        refresh: localStorage.getItem('refresh') || null,
        refreshInterval:null,
        id: null,
        email: null,

    }),
    actions:{
        saveTokens(data) {
            this.access = data.tokens.access
            this.refresh = data.tokens.refresh
            localStorage.setItem('access', data.tokens.access)
            localStorage.setItem('refresh', data.tokens.refresh)
        },

        saveUserData(data) {
            this.id = data.id
            this.email = data.email
            localStorage.setItem('userId', data.id)
            localStorage.setItem('email', data.email)
        },

        async fetchUser() {
          if (!this.accessToken) return

          try {
            const res = await fetch('/api/user/', {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.accessToken}`,
              },
            })

            if (!res.ok) {
              throw new Error('Failed to fetch user')
            }

            const data = await res.json()
            this.saveUserData(data)
          } catch (err) {
            console.error('Error fetching user:', err)
            this.logout()
          }
        },

        async login(email, password) {
            const csrf = getCSRFToken()
            const res = await fetch('http://localhost:8000/api/login/', {
                method: 'POST',
                credentials: 'include',
                headers : {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body : JSON.stringify({email, password}),
            })

            if (!res.ok) throw new Error('Login failed')
            const data = await res.json()
            this.fetchUser()
            this.saveTokens(data)
            this.startRefreshLoop()
        },

        async register(email, password, confirmPassword) {
            const csrf = getCSRFToken()
            const res = await fetch('http://localhost:8000/api/register/', {
                method: 'POST',
                credentials: 'include',
                headers : {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body : JSON.stringify({email, password, confirm_password: confirmPassword}),

            })
            if (!res.ok) throw new Error('Registration failed')
        },

        async refreshToken() {
            console.log("Refresh token being sent:", this.refresh);
            const res = await fetch('http://localhost:8000/api/token/refresh/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({refresh:this.refresh})
            })
            if (!res.ok) {
                this.logout()
                throw new Error("Refresh failed")
            }
        },

        startRefreshLoop() {
            if (this.refreshInterval) clearInterval(this.refreshInterval)
            this.refreshInterval = setInterval(() => {
                if (this.refresh) this.refreshToken()
            }, 1000 * 60 * 5)
        },

        logout() {
            this.access = null
            this.refresh = null
            this.email = null
            this.id = null
            localStorage.clear()
            if (this.refreshInterval) clearInterval(this.refreshInterval)
        },
    },
})
