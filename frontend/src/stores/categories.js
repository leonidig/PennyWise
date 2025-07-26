import { defineStore } from 'pinia'


export const useCategoryStore = defineStore('categories', {
    state: () => ({
        categories: [],
    }),
    actions: {
        async fetchCategories() {
            try {
                const token = localStorage.getItem('access')
                const res = await fetch('http://localhost:8000/api/category/', { headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                      }})
                if (!res.ok) throw new Error('Failed to fetch categories')
                const data = await res.json()
                console.log('Fetched categories:', data)
                this.categories = data
            } catch (error) {
                console.error('Error fetching categories:', error)
            }
        },

        async getCategoryById(id) {
            try {
                const token = localStorage.getItem('access')
                const res = await fetch(`http://localhost:8000/api/category/${id}/`, { headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                      }})
                if (!res.ok) throw new Error('Failed to fetch category')
                return await res.json()
            } catch (error) {
                console.error('Error fetching category:', error)
                return null
            }
        },

        async addCategory(name, is_income) {
            try {
              const token = localStorage.getItem('access')
              if (!token) throw new Error('No access token found')
                const res = await fetch('http://localhost:8000/api/category/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({ name, is_income}),
                })
                if (!res.ok) throw new Error('Failed to add category')
                await this.fetchCategories()
            } catch (error) {
                console.error('Error adding category:', error)
            }
        },
      async updateCategory(name, is_income, id) {
            try {
                const token = localStorage.getItem('access')
                if (!token) throw new Error('No access token found')
                const res = await fetch(`http://localhost:8000/api/category/${id}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({ name, is_income }),
                })
                if (!res.ok) throw new Error('Failed to edit category')
                await this.fetchCategories()
            } catch (error) {
                console.error('Error editing category:', error)
            }
        }
    }
})
