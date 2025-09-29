import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '@/services/auth'

import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import MenusView from '@/views/MenusView.vue'
import MenuFormView from '@/views/MenuFormView.vue'
import OrdersView from '@/views/OrdersView.vue'
import OrderFormView from '@/views/OrderFormView.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/menus',
    name: 'Menus',
    component: MenusView,
    meta: { requiresAuth: true }
  },
  {
    path: '/menus/new',
    name: 'MenuCreate',
    component: MenuFormView,
    meta: { requiresAuth: true }
  },
  {
    path: '/menus/:id/edit',
    name: 'MenuEdit',
    component: MenuFormView,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: OrdersView,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders/new',
    name: 'OrderCreate',
    component: OrderFormView,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders/:id/edit',
    name: 'OrderEdit',
    component: OrderFormView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = await authService.checkAuth()
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router