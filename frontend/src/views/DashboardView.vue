<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar :user="user" @logout="handleLogout" />
    
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p class="mt-2 text-gray-600">Welcome to Restaurant Management System</p>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-primary-500 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Menus</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.totalMenus }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Orders</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.totalOrders }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Pending Orders</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.pendingOrders }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                    <span class="text-white font-bold text-sm">Rp</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Today's Revenue</dt>
                    <dd class="text-lg font-medium text-gray-900">Rp {{ formatCurrency(stats.todayRevenue) }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <!-- Recent Orders -->
          <div class="bg-white shadow rounded-lg">
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Recent Orders</h3>
                <router-link to="/orders" class="text-primary-600 hover:text-primary-500 text-sm font-medium">
                  View all
                </router-link>
              </div>
              
              <div v-if="recentOrders.length === 0" class="text-center text-gray-500 py-4">
                No recent orders
              </div>
              
              <div v-else class="space-y-3">
                <div
                  v-for="order in recentOrders"
                  :key="order.id"
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div>
                    <div class="text-sm font-medium text-gray-900">
                      {{ order.customer_name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      Rp {{ formatCurrency(order.total_amount) }}
                    </div>
                  </div>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="{
                      'bg-yellow-100 text-yellow-800': order.status === 'pending',
                      'bg-green-100 text-green-800': order.status === 'completed',
                      'bg-red-100 text-red-800': order.status === 'cancelled'
                    }"
                  >
                    {{ order.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white shadow rounded-lg">
            <div class="p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
              <div class="space-y-3">
                <router-link
                  to="/menus/new"
                  class="flex items-center p-3 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
                >
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-primary-500 rounded-md flex items-center justify-center">
                      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                    </div>
                  </div>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">Add New Menu</div>
                    <div class="text-sm text-gray-500">Create a new menu item</div>
                  </div>
                </router-link>

                <router-link
                  to="/orders/new"
                  class="flex items-center p-3 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
                >
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                      </svg>
                    </div>
                  </div>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">New Order</div>
                    <div class="text-sm text-gray-500">Create a new order</div>
                  </div>
                </router-link>

                <router-link
                  to="/orders?status=pending"
                  class="flex items-center p-3 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors"
                >
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  </div>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">Manage Orders</div>
                    <div class="text-sm text-gray-500">View and update order status</div>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import { authService } from '@/services/auth'
import { menuService } from '@/services/menu'
import { orderService } from '@/services/order'

export default {
  name: 'DashboardView',
  components: {
    Navbar
  },
  data() {
    return {
      user: null,
      stats: {
        totalMenus: 0,
        totalOrders: 0,
        pendingOrders: 0,
        todayRevenue: 0
      },
      recentOrders: []
    }
  },
  async created() {
    await this.loadUser()
    await this.loadStats()
  },
  methods: {
    async loadUser() {
      try {
        this.user = await authService.getCurrentUser()
      } catch (error) {
        console.error('Failed to load user:', error)
      }
    },
    async loadStats() {
      try {
        // Load menus
        const menusData = await menuService.getMenus({ per_page: 1 })
        this.stats.totalMenus = menusData.total

        // Load orders
        const ordersData = await orderService.getOrders({ per_page: 5 })
        this.stats.totalOrders = ordersData.total
        this.recentOrders = ordersData.orders

        // Count pending orders
        const pendingData = await orderService.getOrders({ status: 'pending', per_page: 1 })
        this.stats.pendingOrders = pendingData.total

        // Calculate today's revenue (simplified - sum of completed orders)
        const completedOrders = await orderService.getOrders({ status: 'completed', per_page: 100 })
        this.stats.todayRevenue = completedOrders.orders.reduce((sum, order) => sum + order.total_amount, 0)
      } catch (error) {
        console.error('Failed to load stats:', error)
      }
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat('id-ID').format(amount)
    },
    handleLogout() {
      this.user = null
    }
  }
}
</script>