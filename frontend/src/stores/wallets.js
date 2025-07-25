import { defineStore } from 'pinia'

export const useWalletStore = defineStore( 'wallets', {
    state: () => ({
        balances: [],
        currencies: [],
    }),

    actions: {
        async fetchWallets() {
            try {
                const res = await fetch('http://localhost:8000/api/wallet')
                const data = await res.json()
                this.balances = data
            } catch (error) {
                console.error('Error fetching wallets:', error)
            }
        },
        async fetchCurrencies() {
            try {
                const res = await fetch('http://localhost:8000/api/currencies/')
                if (!response.ok) throw new Error('Failed to fetch')
                this.currencies = res.data.map(c => c.code)
            } catch (error) {
                console.error('Error fetching currencies:', error)
            }
        }
    }
})