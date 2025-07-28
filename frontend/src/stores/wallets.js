import { defineStore } from 'pinia'
import { convertCurrency } from '@/utils/convertCurrency.js'

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

        async patchWalletBalance(walletId, amount, categoryId) {
          const { useCategoryStore } = await import('@/stores/categories.js')
          const categoryStore = useCategoryStore()
          await categoryStore.fetchCategories()

          const category = await categoryStore.getCategoryById(categoryId)
          if (!category) {
            throw new Error('Category not found')
          }
          const wallet = await this.getWalletById(walletId)
          if (!wallet) {
            throw new Error('Wallet not found')
          }
          if (category.is_income) {
            wallet.balance = parseFloat((Number(wallet.balance) + Number(amount)).toFixed(2))
          } else {
            if (wallet.balance < amount) {
              throw new Error('Insufficient funds')
            }
            wallet.balance = parseFloat((Number(wallet.balance) - Number(amount)).toFixed(2))
          }
          console.log("Patching wallet balance:", wallet.balance, amount, categoryId)
            try {
              const token = localStorage.getItem('access')
              const res = await fetch(`http://localhost:8000/api/wallet/${walletId}/`, {
                method: 'PATCH',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ balance: wallet.balance }),
              })
              if (!res.ok) throw new Error('Failed to update wallet balance')
              const updatedWallet = await res.json()
              await this.fetchWallets()
              return updatedWallet
            } catch (error) {
              console.error('Error updating wallet balance:', error)
              throw error
            }
        },

        async revertWalletBalance(walletId, amount, categoryId) {
          const { useCategoryStore } = await import('@/stores/categories.js')
          const categoryStore = useCategoryStore()
          await categoryStore.fetchCategories()

          const category = await categoryStore.getCategoryById(categoryId)
          if (!category) {
            throw new Error('Category not found')
          }
          const wallet = await this.getWalletById(walletId)
          if (!wallet) {
            throw new Error('Wallet not found')
          }
          if (category.is_income) {
            wallet.balance = parseFloat((Number(wallet.balance) + Number(amount)).toFixed(2))
            if (wallet.balance < 0) {
              wallet.balance = parseFloat((Number(wallet.balance) + Number(amount)).toFixed(2))
              throw new Error('Insufficient funds to revert transaction')
          }
          } else {
            wallet.balance = parseFloat((Number(wallet.balance) + Number(amount)).toFixed(2))
          }
          console.log("Reverting wallet balance:", wallet.balance, amount, categoryId)

            try {
              const token = localStorage.getItem('access')
              const res = await fetch(`http://localhost:8000/api/wallet/${walletId}/`, {
                method: 'PATCH',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ balance: wallet.balance }),
              })
              if (!res.ok) throw new Error('Failed to update wallet balance')
              const updatedWallet = await res.json()
              await this.fetchWallets()
              return updatedWallet
            } catch (error) {
              console.error('Error updating wallet balance:', error)
              throw error
            }
        },

        async updateWallet(id, name, newCurrencyId, newBalance) {
  try {

    const oldWallet = await this.getWalletById(id)
    const oldCurrencyId = oldWallet.currency
    const oldBalance = oldWallet.balance

    if (oldCurrencyId === newCurrencyId) {
      const res = await fetch(`http://localhost:8000/api/wallet/${id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`,
        },
        body: JSON.stringify({ name, currency: newCurrencyId, balance: newBalance }),
      })
      if (!res.ok) throw new Error('Failed to update wallet')
      await this.fetchWallets()
      return
    }


    const fromCode = this.currencies.find(c => c.id === oldCurrencyId).code
    const toCode = this.currencies.find(c => c.id === newCurrencyId).code
      // const currenciesUsed = this.currencies.value.map(c => c.code).join(',')
    // const rateRes = await fetch(
    //   `https://api.exchangerate.host/live?access_key=bcdae7fbdec58e47ad6d16dede76db0c&source=EUR&currencies=${currenciesUsed}`
    // )
    // const exchangeRates = await rateRes.json()
    const exchangeRates = {
      quotes: {
        'EURUSD': 1.1,
        'EURUAH': 130.0,
        'EURBTC': 0.9,
      }
    }

    const convertedBalance = parseFloat(
      convertCurrency(oldBalance, fromCode, toCode, exchangeRates.quotes).toFixed(2)
    )

    const res = await fetch(`http://localhost:8000/api/wallet/${id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
      },
      body: JSON.stringify({ name, currency: newCurrencyId, balance: convertedBalance }),
    })
    if (!res.ok) throw new Error('Failed to update wallet')


    const { useTransactionStore } = await import('@/stores/transactions')
    const transactionStore = useTransactionStore()
    await transactionStore.fetchTransactions()

    const relatedTransactions = transactionStore.transactions.filter(t => t.wallet === id)
    for (const t of relatedTransactions) {
      const convertedAmount = parseFloat(
        convertCurrency(t.amount, fromCode, toCode, exchangeRates.quotes).toFixed(0)
      )
      await fetch(`http://localhost:8000/api/transaction/${t.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`,
        },
        body: JSON.stringify({
          amount: convertedAmount,
          currency: newCurrencyId,
        })
      })
    }

    await this.fetchWallets()
    await transactionStore.fetchTransactions()

  } catch (error) {
    console.error('Error updating wallet and converting transactions:', error)
  }
},


        async deleteWallet(id) {
            try {
                const token = localStorage.getItem('access')
                const res = await fetch(`http://localhost:8000/api/wallet/${id}/`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                })
                if (!res.ok) throw new Error('Failed to delete wallet')
                await this.fetchWallets()
            } catch (error) {
                console.error('Error deleting wallet:', error)
            }
        },


    }
})
