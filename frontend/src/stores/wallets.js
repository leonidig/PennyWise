import { defineStore } from 'pinia'

export const useWalletStore = defineStore( 'wallets', {
    state: () => ({
        balances: [],
        currencies: [],
        token: localStorage.getItem('access') || null,
    }),

    actions: {
        async fetchWallets() {
            try {
                const res = await fetch('http://localhost:8000/api/wallet/', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`,
                    }
                })

                const data = await res.json()
                this.balances = data
            } catch (error) {
                console.error('Error fetching wallets:', error)
            }
        },
        async fetchCurrencies() {
            // try {
            //     const token = localStorage.getItem('access')
            //     const res = await fetch('http://localhost:8000/api/currency/', {
            //       method: 'GET',
            //             headers: {
            //             'Authorization': `Bearer ${token}`,
            //           }})
            //     if (!res.ok) throw new Error('Failed to fetch')
            //     this.currencies = res.data
            // } catch (error) {
            //     console.error('Error fetching currencies:', error)
            // }
            this.currencies = [
            {"id":1, "code": "USD", "symbol": "$"},
            {"id":2, "code": "EUR", "symbol": "€"},
            {"id":3, "code": "UAH", "symbol": "₴"},
            {"id":4, "code": "BTC", "symbol": "₿"},
        ]
        },
        async addWallet(name, balance, currency) {
            try {
                const token = localStorage.getItem('access')
                const res = await fetch('http://localhost:8000/api/wallet/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({name, balance, currency}),
                })
                if (!res.ok) throw new Error('Failed to add wallet')
                await this.fetchWallets()
            } catch (error) {
                console.error('Error adding wallet:', error)
            }
        },

        async getWalletById(id) {
            try {
                const res = await fetch(`http://localhost:8000/api/wallet/${id}/`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`,
                    }
                })
                if (!res.ok) throw new Error('Failed to fetch wallet')
                return await res.json()
            } catch (error) {
                console.error('Error fetching wallet:', error)
                return null
            }
        },


    }
})
