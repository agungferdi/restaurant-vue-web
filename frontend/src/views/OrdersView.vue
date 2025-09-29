<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar :user="user" @logout="handleLogout" />
    
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Header -->
        <div class="flex justify-between items-center mb-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Order Management</h1>
            <p class="mt-2 text-gray-600">Manage customer orders and track their status</p>
          </div>
          <router-link
            to="/orders/new"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Order
          </router-link>
        </div>

        <!-- Filter and Search -->
        <div class="bg-white p-6 rounded-lg shadow mb-6">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Search Customer</label>
              <input
                v-model="searchQuery"
                @input="handleSearch"
                type="text"
                placeholder="Search by customer name..."
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
              <select
                v-model="selectedStatus"
                @change="handleFilter"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="">All Status</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Per Page</label>
              <select
                v-model="perPage"
                @change="handleFilter"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
              </select>
            </div>
            <div class="flex items-end">
              <button
                @click="loadOrders"
                class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md"
              >
                Refresh
              </button>
            </div>
          </div>
        </div>

        <!-- Orders List -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p class="mt-2 text-gray-600">Loading orders...</p>
        </div>

        <div v-else-if="orders.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No orders found</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new order.</p>
          <div class="mt-6">
            <router-link
              to="/orders/new"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              New Order
            </router-link>
          </div>
        </div>

        <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
          <ul class="divide-y divide-gray-200">
            <li
              v-for="order in orders"
              :key="order.id"
              class="hover:bg-gray-50"
            >
              <div class="px-6 py-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="flex-shrink-0">
                      <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                        <span class="text-primary-600 font-medium text-sm">#{{ order.id }}</span>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="flex items-center">
                        <h3 class="text-lg font-medium text-gray-900">{{ order.customer_name }}</h3>
                        <span
                          class="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          :class="{
                            'bg-yellow-100 text-yellow-800': order.status === 'pending',
                            'bg-green-100 text-green-800': order.status === 'completed',
                            'bg-red-100 text-red-800': order.status === 'cancelled'
                          }"
                        >
                          {{ order.status }}
                        </span>
                      </div>
                      <div class="mt-1 text-sm text-gray-600">
                        <div class="flex items-center space-x-4">
                          <span>Rp {{ formatCurrency(order.total_amount) }}</span>
                          <span>{{ order.order_items.length }} items</span>
                          <span>{{ formatDate(order.created_at) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <!-- Status Update Buttons - Only show for pending orders -->
                    <div v-if="order.status === 'pending'" class="flex space-x-1">
                      <button
                        @click="updateOrderStatus(order.id, 'completed')"
                        class="bg-green-600 hover:bg-green-700 text-white text-xs font-medium py-1 px-3 rounded"
                      >
                        Complete
                      </button>
                      <button
                        @click="updateOrderStatus(order.id, 'cancelled')"
                        class="bg-red-600 hover:bg-red-700 text-white text-xs font-medium py-1 px-3 rounded"
                      >
                        Cancel
                      </button>
                    </div>
                    
                    <!-- Edit and Delete buttons always visible -->
                    <router-link
                      :to="`/orders/${order.id}/edit`"
                      class="bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium py-1 px-3 rounded"
                    >
                      Edit
                    </router-link>
                    <button
                      @click="confirmDelete(order)"
                      class="bg-red-600 hover:bg-red-700 text-white text-xs font-medium py-1 px-3 rounded"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                
                <!-- Order Items -->
                <div v-if="order.order_items.length > 0" class="mt-4">
                  <div class="bg-gray-50 rounded-lg p-3">
                    <h4 class="text-sm font-medium text-gray-700 mb-2">Order Items:</h4>
                    <div class="space-y-1">
                      <div
                        v-for="item in order.order_items"
                        :key="item.id"
                        class="flex justify-between items-center text-sm"
                      >
                        <span class="text-gray-600">{{ item.menu_name }} x{{ item.quantity }}</span>
                        <span class="font-medium">Rp {{ formatCurrency(item.subtotal) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Notes -->
                <div v-if="order.notes" class="mt-3">
                  <p class="text-sm text-gray-600">
                    <span class="font-medium">Notes:</span> {{ order.notes }}
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-8 flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Previous
            </button>
            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing {{ (currentPage - 1) * perPage + 1 }} to {{ Math.min(currentPage * perPage, totalItems) }} of {{ totalItems }} results
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="changePage(currentPage - 1)"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  Previous
                </button>
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="changePage(page)"
                  :class="{
                    'z-10 bg-primary-50 border-primary-500 text-primary-600': page === currentPage,
                    'bg-white border-gray-300 text-gray-500 hover:bg-gray-50': page !== currentPage
                  }"
                  class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
                >
                  {{ page }}
                </button>
                <button
                  @click="changePage(currentPage + 1)"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  Next
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      :show="deleteDialog.show"
      title="Delete Order"
      :message="`Are you sure you want to delete order #${deleteDialog.order?.id} from '${deleteDialog.order?.customer_name}'? This action cannot be undone.`"
      @close="deleteDialog.show = false"
      @confirm="handleDelete"
    />

    <!-- Alert Dialog -->
    <AlertDialog
      :show="alert.show"
      :type="alert.type"
      :title="alert.title"
      :message="alert.message"
      @close="alert.show = false"
    />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import AlertDialog from '@/components/AlertDialog.vue'
import { authService } from '@/services/auth'
import { orderService } from '@/services/order'

export default {
  name: 'OrdersView',
  components: {
    Navbar,
    ConfirmDialog,
    AlertDialog
  },
  data() {
    return {
      user: null,
      orders: [],
      loading: false,
      searchQuery: '',
      selectedStatus: '',
      perPage: 10,
      currentPage: 1,
      totalPages: 0,
      totalItems: 0,
      searchTimeout: null,
      deleteDialog: {
        show: false,
        order: null
      },
      alert: {
        show: false,
        type: 'success',
        title: '',
        message: ''
      }
    }
  },
  computed: {
    visiblePages() {
      const range = 2
      const start = Math.max(1, this.currentPage - range)
      const end = Math.min(this.totalPages, this.currentPage + range)
      
      const pages = []
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    }
  },
  async created() {
    await this.loadUser()
    await this.loadOrders()
  },
  methods: {
    async loadUser() {
      try {
        this.user = await authService.getCurrentUser()
      } catch (error) {
        console.error('Failed to load user:', error)
      }
    },
    async loadOrders() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          per_page: this.perPage
        }
        
        if (this.searchQuery) {
          params.search = this.searchQuery
        }
        
        if (this.selectedStatus) {
          params.status = this.selectedStatus
        }
        
        const data = await orderService.getOrders(params)
        this.orders = data.orders
        this.totalPages = data.pages
        this.totalItems = data.total
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to load orders')
      } finally {
        this.loading = false
      }
    },
    handleSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.currentPage = 1
        this.loadOrders()
      }, 300)
    },
    handleFilter() {
      this.currentPage = 1
      this.loadOrders()
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.loadOrders()
      }
    },
    async updateOrderStatus(orderId, status) {
      try {
        await orderService.updateOrderStatus(orderId, status)
        this.showAlert('success', 'Success', `Order status updated to ${status}`)
        await this.loadOrders()
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to update order status')
      }
    },
    confirmDelete(order) {
      this.deleteDialog.order = order
      this.deleteDialog.show = true
    },
    async handleDelete() {
      try {
        await orderService.deleteOrder(this.deleteDialog.order.id)
        this.showAlert('success', 'Success', 'Order deleted successfully')
        this.deleteDialog.show = false
        await this.loadOrders()
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to delete order')
      }
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat('id-ID').format(amount)
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    showAlert(type, title, message) {
      this.alert = { show: true, type, title, message }
    },
    handleLogout() {
      this.user = null
    }
  }
}
</script>