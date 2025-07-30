import { defineStore } from 'pinia'
import { convertCurrency } from '@/utils/convertCurrency.js'

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






        async addTransaction(walletId, amount, comment, categoryId) {
          const { useWalletStore } = await import('@/stores/wallets.js')
          const wallets = useWalletStore()
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
                await wallets.fetchWallets()
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
        },

        async updateTransaction(id, newWalletId, newAmount, newComment, newCategoryId) {
  const { useWalletStore } = await import('@/stores/wallets.js')
  const wallets = useWalletStore()
  await wallets.fetchWallets()

  const transaction = await this.getTransactionById(id)
  if (!transaction) throw new Error('Transaction not found')

  const currencies = wallets.currencies
  const oldWalletId = transaction.wallet
  const oldWallet = await wallets.getWalletById(oldWalletId)
  const oldAmount = transaction.amount
  const oldCategoryId = transaction.category
  const oldCurrency = currencies.find(c => c.id == oldWallet.currency).code

  const newWallet = await wallets.getWalletById(newWalletId)
  const newCurrency = currencies.find(c => c.id == newWallet.currency).code
          // const currenciesUsed = wallets.currencies.value.map(c => c.code).join(',')
          // const rateRes = await fetch(
          //   `https://api.exchangerate.host/live?access_key=bcdae7fbdec58e47ad6d16dede76db0c&source=EUR&currencies=${currenciesUsed}`
          // )
          // const rateData = await rateRes.json()

  const rateData = {
    success: true,
    quotes: {
      'EURUSD': 1.1,
      'EURBTC': 0.9,
      'EURUAH': 130.0,
    }
  }

  const quotes = rateData.quotes
  let finalAmount = newAmount

  if (newWalletId !== oldWalletId) {
    await wallets.revertWalletBalance(oldWalletId, oldAmount, oldCategoryId)

    const convertedAmount = parseFloat(
      convertCurrency(oldAmount, oldCurrency, newCurrency, quotes).toFixed(0)
    )
    console.log("Converted amount:", convertedAmount)

    await wallets.patchWalletBalance(newWalletId, convertedAmount, newCategoryId)
    finalAmount = convertedAmount
  } else {
    if (newAmount !== oldAmount) {
      const delta = newAmount - oldAmount
      const isIncome = ((await import('@/stores/categories')).useCategoryStore()).categories.find(c => c.id === oldCategoryId)?.is_income

      if (isIncome) {
        oldWallet.balance += delta
      } else {
        oldWallet.balance -= delta
      }

      await fetch(`http://localhost:8000/api/wallet/${oldWalletId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`,
        },
        body: JSON.stringify({ balance: oldWallet.balance }),
      })
    }

    if (newCategoryId !== oldCategoryId) {
      await wallets.revertWalletBalance(oldWalletId, oldAmount, oldCategoryId)
      await wallets.patchWalletBalance(oldWalletId, oldAmount, newCategoryId)
    }
  }

  try {
    const res = await fetch(`http://localhost:8000/api/transaction/${id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
      },
      body: JSON.stringify({
        wallet: newWalletId,
        category: newCategoryId,
        amount: finalAmount,
        comment: newComment,
      }),
    })
    if (!res.ok) throw new Error('Failed to update transaction')
    await this.fetchTransactions()
  } catch (error) {
    console.error('Error updating transaction:', error)
  }
},



        async deleteTransaction(id) {
            const { useWalletStore } = await import('@/stores/wallets.js')
            const wallets = useWalletStore()
            const transaction = await this.getTransactionById(id)
            if (!transaction) {
                console.error('Transaction not found')
                return
            }
            const walletId = transaction.wallet
            const amount = transaction.amount
            const categoryId = transaction.category

            try {
                const res = await fetch(`http://localhost:8000/api/transaction/${id}/`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`,
                    },
                })
                if (!res.ok) throw new Error('Failed to delete transaction')
                await this.fetchTransactions()
                wallets.revertWalletBalance(walletId, amount, categoryId)
            } catch (error) {
                console.error('Error deleting transaction:', error)
            }
        },
    }
})
