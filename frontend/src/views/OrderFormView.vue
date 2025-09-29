<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar :user="user" @logout="handleLogout" />
    
    <main class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Header -->
        <div class="mb-6">
          <router-link to="/orders" class="text-primary-600 hover:text-primary-500 text-sm font-medium">
            ← Back to Orders
          </router-link>
          <h1 class="mt-2 text-3xl font-bold text-gray-900">
            {{ isEdit ? 'Edit Order' : 'New Order' }}
          </h1>
          <p class="mt-2 text-gray-600">
            {{ isEdit ? 'Update order information' : 'Create a new order for customer' }}
          </p>
        </div>

        <!-- Form -->
        <div class="bg-white shadow rounded-lg">
          <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
            <!-- Customer Information -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">Customer Information</h3>
              <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div class="sm:col-span-1">
                  <label for="customer_name" class="block text-sm font-medium text-gray-700">
                    Customer Name *
                  </label>
                  <div class="mt-1">
                    <input
                      id="customer_name"
                      v-model="form.customer_name"
                      type="text"
                      required
                      class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                      placeholder="Enter customer name"
                    />
                  </div>
                  <div v-if="errors.customer_name" class="mt-1 text-sm text-red-600">{{ errors.customer_name }}</div>
                </div>

                <div class="sm:col-span-1">
                  <label for="status" class="block text-sm font-medium text-gray-700">
                    Status
                  </label>
                  <div class="mt-1">
                    <select
                      id="status"
                      v-model="form.status"
                      class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    >
                      <option value="pending">Pending</option>
                      <option value="completed">Completed</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </div>
                </div>

                <div class="sm:col-span-2">
                  <label for="notes" class="block text-sm font-medium text-gray-700">
                    Notes
                  </label>
                  <div class="mt-1">
                    <textarea
                      id="notes"
                      v-model="form.notes"
                      rows="3"
                      class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                      placeholder="Any special instructions or notes..."
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>

            <!-- Order Items -->
            <div>
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-medium text-gray-900">Order Items</h3>
                <button
                  type="button"
                  @click="addOrderItem"
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Add Item
                </button>
              </div>

              <div v-if="form.items.length === 0" class="text-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900">No items added</h3>
                <p class="mt-1 text-sm text-gray-500">Add menu items to this order.</p>
              </div>

              <div v-else class="space-y-4">
                <div
                  v-for="(item, index) in form.items"
                  :key="index"
                  class="bg-gray-50 p-4 rounded-lg border"
                >
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
                    <div class="sm:col-span-2">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Menu Item *</label>
                      <select
                        v-model="item.menu_id"
                        @change="updateItemPrice(index)"
                        required
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      >
                        <option value="">Select Menu</option>
                        <option
                          v-for="menu in availableMenus"
                          :key="menu.id"
                          :value="menu.id"
                          :disabled="!menu.is_available"
                        >
                          {{ menu.name }} - Rp {{ formatCurrency(menu.price) }}
                          {{ !menu.is_available ? ' (Unavailable)' : '' }}
                        </option>
                      </select>
                    </div>
                    
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">Quantity *</label>
                      <input
                        v-model="item.quantity"
                        type="number"
                        min="1"
                        required
                        @input="updateItemSubtotal(index)"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      />
                    </div>
                    
                    <div class="flex items-end justify-between">
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Subtotal</label>
                        <div class="text-lg font-medium text-gray-900">
                          Rp {{ formatCurrency(item.subtotal || 0) }}
                        </div>
                      </div>
                      <button
                        type="button"
                        @click="removeOrderItem(index)"
                        class="ml-2 inline-flex items-center p-1 border border-transparent rounded-full shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                      >
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="errors.items" class="mt-2 text-sm text-red-600">{{ errors.items }}</div>
            </div>

            <!-- Order Summary -->
            <div v-if="form.items.length > 0" class="border-t pt-6">
              <div class="bg-gray-50 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-900 mb-3">Order Summary</h4>
                <div class="space-y-2">
                  <div
                    v-for="(item, index) in form.items"
                    :key="index"
                    class="flex justify-between text-sm"
                  >
                    <span class="text-gray-600">
                      {{ getMenuName(item.menu_id) }} x{{ item.quantity }}
                    </span>
                    <span class="font-medium">Rp {{ formatCurrency(item.subtotal || 0) }}</span>
                  </div>
                  <div class="border-t pt-2 mt-2">
                    <div class="flex justify-between text-lg font-medium">
                      <span>Total</span>
                      <span>Rp {{ formatCurrency(totalAmount) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Form Error -->
            <div v-if="formError" class="rounded-md bg-red-50 p-4">
              <div class="text-sm text-red-800">{{ formError }}</div>
            </div>

            <!-- Actions -->
            <div class="flex justify-end space-x-3 border-t pt-6">
              <router-link
                to="/orders"
                class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Cancel
              </router-link>
              <button
                type="submit"
                :disabled="loading || form.items.length === 0"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                <span v-if="loading">{{ isEdit ? 'Updating...' : 'Creating...' }}</span>
                <span v-else>{{ isEdit ? 'Update Order' : 'Create Order' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>

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
import AlertDialog from '@/components/AlertDialog.vue'
import { authService } from '@/services/auth'
import { orderService } from '@/services/order'
import { menuService } from '@/services/menu'

export default {
  name: 'OrderFormView',
  components: {
    Navbar,
    AlertDialog
  },
  data() {
    return {
      user: null,
      isEdit: false,
      orderId: null,
      availableMenus: [],
      form: {
        customer_name: '',
        status: 'pending',
        notes: '',
        items: []
      },
      errors: {},
      formError: '',
      loading: false,
      alert: {
        show: false,
        type: 'success',
        title: '',
        message: ''
      }
    }
  },
  computed: {
    totalAmount() {
      return this.form.items.reduce((total, item) => total + (item.subtotal || 0), 0)
    }
  },
  async created() {
    await this.loadUser()
    await this.loadMenus()
    
    if (this.$route.params.id) {
      this.isEdit = true
      this.orderId = parseInt(this.$route.params.id)
      await this.loadOrder()
    }
  },
  methods: {
    async loadUser() {
      try {
        this.user = await authService.getCurrentUser()
      } catch (error) {
        console.error('Failed to load user:', error)
      }
    },
    async loadMenus() {
      try {
        const data = await menuService.getMenus({ per_page: 100 })
        this.availableMenus = data.menus
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to load menus')
      }
    },
    async loadOrder() {
      try {
        const order = await orderService.getOrder(this.orderId)
        this.form = {
          customer_name: order.customer_name,
          status: order.status,
          notes: order.notes || '',
          items: order.order_items.map(item => ({
            menu_id: item.menu_id,
            quantity: item.quantity,
            price: item.price,
            subtotal: item.subtotal
          }))
        }
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to load order')
        this.$router.push('/orders')
      }
    },
    addOrderItem() {
      this.form.items.push({
        menu_id: '',
        quantity: 1,
        price: 0,
        subtotal: 0
      })
    },
    removeOrderItem(index) {
      this.form.items.splice(index, 1)
    },
    updateItemPrice(index) {
      const item = this.form.items[index]
      const menu = this.availableMenus.find(m => m.id === parseInt(item.menu_id))
      if (menu) {
        item.price = menu.price
        this.updateItemSubtotal(index)
      }
    },
    updateItemSubtotal(index) {
      const item = this.form.items[index]
      item.subtotal = (item.price || 0) * (item.quantity || 0)
    },
    getMenuName(menuId) {
      const menu = this.availableMenus.find(m => m.id === parseInt(menuId))
      return menu ? menu.name : 'Unknown Menu'
    },
    validateForm() {
      this.errors = {}
      this.formError = ''

      if (!this.form.customer_name.trim()) {
        this.errors.customer_name = 'Customer name is required'
      }

      if (this.form.items.length === 0) {
        this.errors.items = 'At least one menu item is required'
      }

      // Validate each item
      for (let i = 0; i < this.form.items.length; i++) {
        const item = this.form.items[i]
        if (!item.menu_id) {
          this.errors.items = 'Please select a menu for all items'
          break
        }
        if (!item.quantity || item.quantity <= 0) {
          this.errors.items = 'Quantity must be greater than 0 for all items'
          break
        }
      }

      return Object.keys(this.errors).length === 0
    },
    async handleSubmit() {
      if (!this.validateForm()) {
        return
      }

      this.loading = true

      try {
        const orderData = {
          customer_name: this.form.customer_name,
          status: this.form.status,
          notes: this.form.notes,
          items: this.form.items.map(item => ({
            menu_id: parseInt(item.menu_id),
            quantity: parseInt(item.quantity)
          }))
        }

        if (this.isEdit) {
          await orderService.updateOrder(this.orderId, orderData)
          this.showAlert('success', 'Success', 'Order updated successfully')
        } else {
          await orderService.createOrder(orderData)
          this.showAlert('success', 'Success', 'Order created successfully')
        }

        setTimeout(() => {
          this.$router.push('/orders')
        }, 1500)
      } catch (error) {
        this.formError = error.error || `Failed to ${this.isEdit ? 'update' : 'create'} order`
        
        // Handle validation errors
        if (error.details && typeof error.details === 'object') {
          this.errors = error.details
        }
      } finally {
        this.loading = false
      }
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat('id-ID').format(amount)
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