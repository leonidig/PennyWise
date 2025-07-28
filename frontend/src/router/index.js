import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Wallets from '@/views/wallet/Wallets.vue'
import Transactions from '@/views/transaction/Transactions.vue'
import WalletInfo from '@/views/wallet/WalletInfo.vue'
import TransactionInfo from '@/views/transaction/TransactionInfo.vue'
import Profile from '@/views/Profile.vue'
import EditWallet from '@/views/wallet/EditWallet.vue'
import EditTransactions from '@/views/transaction/EditTransactions.vue'
import AddWallet from '@/views/wallet/AddWallet.vue'
import AddTransaction from '@/views/transaction/AddTransaction.vue'
import AddCategory from '@/views/category/AddCategory.vue'
import EditCategory from '@/views/category/EditCategory.vue'
import Categories from '@/views/category/Categories.vue'

const routes = [
    { path: "/", name: 'Home', component: Home, meta : {requiresAuth: true} },
    { path: "/login", name: "Login", component: Login },
    { path: "/register", name: "Register", component: Register },
    { path: "/wallets", name: "Wallets", component: Wallets, meta : {requiresAuth: true} },
    { path: "/transactions", name: "Transactions", component: Transactions, meta : {requiresAuth: true} },
    { path: "/wallets/:id", name: "WalletInfo", component: WalletInfo, meta : {requiresAuth: true} },
    { path: "/transactions/:id", name: "TransactionInfo", component: TransactionInfo, meta : {requiresAuth: true} },
    { path: "/profile", name: "Profile", component: Profile, meta : {requiresAuth: true} },
    { path: "/wallets/edit/:id", name: "EditWallet", component: EditWallet, meta : {requiresAuth: true} },
    { path: "/transactions/:id/edit", name: "EditTransaction", component: EditTransactions, meta : {requiresAuth: true} },
    { path: "/wallets/add", name: "AddWallet", component: AddWallet, meta : {requiresAuth: true} },
    { path: "/transactions/add", name: "AddTransaction", component: AddTransaction, meta : {requiresAuth: true} },
    { path: "/categories/add", name: "AddCategory", component: AddCategory, meta : {requiresAuth: true} },
    { path: "/categories/edit/:id", name: "EditCategory", component: EditCategory, meta : {requiresAuth: true} },
    { path: "/categories", name: "Categories", component: Categories, meta : {requiresAuth: true} }
]



const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  console.log("Access token in router:", auth.access)
  console.log("Refresh token in router:", auth.refresh)
  if (to.meta.requiresAuth && !auth.access ) {
    return '/login'
  }
})
export default router
