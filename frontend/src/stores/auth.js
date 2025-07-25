import { defineStore } from 'pinia'
import { getCSRFToken } from '../utils/csrf'



export const useAuthStore = defineStore('auth', {
    state: () => ({
        access: localStorage.getItem('access') || null,
        refresh: localStorage.getItem('refresh') || null,
        user: null,
        refreshInterval:null
    }),
    actions:{
        saveTokens(data) {
            this.access = data.tokens.access
            this.refresh = data.tokens.refresh
            localStorage.setItem('access', data.access)
            localStorage.setItem('refresh', data.refresh)
        },

        async login(email, password) {
            const csrf = getCSRFToken()

            const res = await fetch('http://localhost:8000/api/login', {
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
            this.saveTokens(data)

            this.startRefreshLoop()
        },

        async register(email, password, confirmPassword) {
            const csrf = getCSRFToken()
            const res = await fetch('http://localhost:8000/api/register', {
                mehtod: 'POST',
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
            const res = await fetch('http://localhost:8000/api/token/refresh', {
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
            this.user = null
            localStorage.clear()
            if (this.refreshInterval) clearInterval(this.refreshInterval)
        },
    },
})
