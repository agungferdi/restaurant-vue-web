<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar :user="user" @logout="handleLogout" />
    
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Header -->
        <div class="flex justify-between items-center mb-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Menu Management</h1>
            <p class="mt-2 text-gray-600">Manage your restaurant menu items</p>
          </div>
          <router-link
            to="/menus/new"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Add Menu
          </router-link>
        </div>

        <!-- Search and Filter -->
        <div class="bg-white p-6 rounded-lg shadow mb-6">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <input
                v-model="searchQuery"
                @input="handleSearch"
                type="text"
                placeholder="Search menus..."
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                v-model="selectedCategory"
                @change="handleFilter"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="">All Categories</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
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
          </div>
        </div>

        <!-- Menus Grid -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p class="mt-2 text-gray-600">Loading menus...</p>
        </div>

        <div v-else-if="menus.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No menus found</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new menu item.</p>
          <div class="mt-6">
            <router-link
              to="/menus/new"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Add Menu
            </router-link>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="menu in menus"
            :key="menu.id"
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div class="aspect-w-16 aspect-h-9">
              <img
                v-if="menu.image_url"
                :src="menu.image_url"
                :alt="menu.name"
                class="w-full h-48 object-cover"
              />
              <div v-else class="w-full h-48 bg-gray-200 flex items-center justify-center">
                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="p-4">
              <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-semibold text-gray-900">{{ menu.name }}</h3>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-800': menu.is_available,
                    'bg-red-100 text-red-800': !menu.is_available
                  }"
                >
                  {{ menu.is_available ? 'Available' : 'Unavailable' }}
                </span>
              </div>
              <p class="text-gray-600 text-sm mb-2">{{ menu.description }}</p>
              <div class="flex justify-between items-center mb-4">
                <div>
                  <span class="text-lg font-bold text-primary-600">Rp {{ formatCurrency(menu.price) }}</span>
                  <div class="text-sm text-gray-500">{{ menu.category }}</div>
                </div>
              </div>
              <div class="flex space-x-2">
                <router-link
                  :to="`/menus/${menu.id}/edit`"
                  class="flex-1 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium py-2 px-4 rounded text-center"
                >
                  Edit
                </router-link>
                <button
                  @click="confirmDelete(menu)"
                  class="flex-1 bg-red-600 hover:bg-red-700 text-white text-sm font-medium py-2 px-4 rounded"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
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
      title="Delete Menu"
      :message="`Are you sure you want to delete '${deleteDialog.menu?.name}'? This action cannot be undone.`"
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
import { menuService } from '@/services/menu'

export default {
  name: 'MenusView',
  components: {
    Navbar,
    ConfirmDialog,
    AlertDialog
  },
  data() {
    return {
      user: null,
      menus: [],
      categories: [],
      loading: false,
      searchQuery: '',
      selectedCategory: '',
      perPage: 10,
      currentPage: 1,
      totalPages: 0,
      totalItems: 0,
      searchTimeout: null,
      deleteDialog: {
        show: false,
        menu: null
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
    await this.loadCategories()
    await this.loadMenus()
  },
  methods: {
    async loadUser() {
      try {
        this.user = await authService.getCurrentUser()
      } catch (error) {
        console.error('Failed to load user:', error)
      }
    },
    async loadCategories() {
      try {
        this.categories = await menuService.getCategories()
      } catch (error) {
        console.error('Failed to load categories:', error)
      }
    },
    async loadMenus() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          per_page: this.perPage
        }
        
        if (this.searchQuery) {
          params.search = this.searchQuery
        }
        
        if (this.selectedCategory) {
          params.category = this.selectedCategory
        }
        
        const data = await menuService.getMenus(params)
        this.menus = data.menus
        this.totalPages = data.pages
        this.totalItems = data.total
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to load menus')
      } finally {
        this.loading = false
      }
    },
    handleSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.currentPage = 1
        this.loadMenus()
      }, 300)
    },
    handleFilter() {
      this.currentPage = 1
      this.loadMenus()
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.loadMenus()
      }
    },
    confirmDelete(menu) {
      this.deleteDialog.menu = menu
      this.deleteDialog.show = true
    },
    async handleDelete() {
      try {
        await menuService.deleteMenu(this.deleteDialog.menu.id)
        this.showAlert('success', 'Success', 'Menu deleted successfully')
        this.deleteDialog.show = false
        await this.loadMenus()
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to delete menu')
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