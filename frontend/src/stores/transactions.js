import { defineStore } from 'pinia'

export const useTransactionStore = defineStore( 'transactions', {
    state: () => ({
        transactions: [],
        token: localStorage.getItem('access') || null,
    }),

    actions: {
        async fetchTransactions() {
            try {

                const res = await fetch('http://localhost:8000/api/transaction/', { headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`,
                      }})
                const data = await res.json()
                this.transactions = data
            } catch (error) {
                console.error('Error fetching wallets:', error)
            }
        },

        // async implementTransaction(walletId, amount, comment, categoryId) {
        //     try {
        //       const token = localStorage.getItem('access')
        //       const res = await fetch(`http://localhost:8000/api/wallet/${walletId}`, {
        //         method: 'PATCH',
        //         headers: {
        //           'Content-Type': 'application/json',
        //           'Authorization': `Bearer ${token}`,
        //         },
        //         body: JSON.stringify({ balance: amount }),
        //       })
        //       if (!res.ok) throw new Error('Failed to update wallet balance')


        async addTransaction(walletId, amount, comment, categoryId) {
            try {
                const res = await fetch('http://localhost:8000/api/transaction/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`,
                    },
                    body: JSON.stringify({ wallet: walletId, category:categoryId, amount, comment }),
                })
                if (!res.ok) throw new Error('Failed to add transaction')
                await this.fetchTransactions()
            } catch (error) {
                console.error('Error adding transaction:', error)
            }
        },

        async getTransactionById(id) {
            try {
                const res = await fetch(`http://localhost:8000/api/transaction/${id}/`, { headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`,
                      }})
                if (!res.ok) throw new Error('Failed to fetch transaction')
                return await res.json()
            } catch (error) {
                console.error('Error fetching transaction:', error)
                return null
            }
        }
    }
})
