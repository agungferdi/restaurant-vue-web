<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar :user="user" @logout="handleLogout" />
    
    <main class="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Header -->
        <div class="mb-6">
          <router-link to="/menus" class="text-primary-600 hover:text-primary-500 text-sm font-medium">
            ← Back to Menus
          </router-link>
          <h1 class="mt-2 text-3xl font-bold text-gray-900">
            {{ isEdit ? 'Edit Menu' : 'Add New Menu' }}
          </h1>
          <p class="mt-2 text-gray-600">
            {{ isEdit ? 'Update menu item information' : 'Create a new menu item for your restaurant' }}
          </p>
        </div>

        <!-- Form -->
        <div class="bg-white shadow rounded-lg">
          <form @submit.prevent="handleSubmit" class="space-y-6 p-6">
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <!-- Name -->
              <div class="sm:col-span-2">
                <label for="name" class="block text-sm font-medium text-gray-700">
                  Menu Name *
                </label>
                <div class="mt-1">
                  <input
                    id="name"
                    v-model="form.name"
                    type="text"
                    required
                    class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    placeholder="e.g., Nasi Goreng Special"
                  />
                </div>
                <div v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</div>
              </div>

              <!-- Category -->
              <div>
                <label for="category" class="block text-sm font-medium text-gray-700">
                  Category *
                </label>
                <div class="mt-1">
                  <select
                    id="category"
                    v-model="form.category"
                    required
                    class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  >
                    <option value="">Select Category</option>
                    <option v-for="category in categories" :key="category" :value="category">
                      {{ category }}
                    </option>
                    <option value="custom">Add New Category</option>
                  </select>
                </div>
                <div v-if="errors.category" class="mt-1 text-sm text-red-600">{{ errors.category }}</div>
              </div>

              <!-- Custom Category Input -->
              <div v-if="form.category === 'custom'">
                <label for="custom-category" class="block text-sm font-medium text-gray-700">
                  New Category *
                </label>
                <div class="mt-1">
                  <input
                    id="custom-category"
                    v-model="customCategory"
                    type="text"
                    required
                    class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    placeholder="Enter new category name"
                  />
                </div>
              </div>

              <!-- Price -->
              <div>
                <label for="price" class="block text-sm font-medium text-gray-700">
                  Price (Rp) *
                </label>
                <div class="mt-1 relative rounded-md shadow-sm">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span class="text-gray-500 sm:text-sm">Rp</span>
                  </div>
                  <input
                    id="price"
                    v-model="form.price"
                    type="number"
                    min="0"
                    step="1000"
                    required
                    class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full pl-12 sm:text-sm border-gray-300 rounded-md"
                    placeholder="25000"
                  />
                </div>
                <div v-if="errors.price" class="mt-1 text-sm text-red-600">{{ errors.price }}</div>
              </div>

              <!-- Description -->
              <div class="sm:col-span-2">
                <label for="description" class="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <div class="mt-1">
                  <textarea
                    id="description"
                    v-model="form.description"
                    rows="3"
                    class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    placeholder="Describe your menu item..."
                  ></textarea>
                </div>
                <p class="mt-2 text-sm text-gray-500">Brief description of the menu item.</p>
                <div v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</div>
              </div>

              <!-- Image Upload -->
              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-700">
                  Menu Image
                </label>
                <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div class="space-y-1 text-center">
                    <div v-if="form.image_url" class="mb-4">
                      <img :src="form.image_url" :alt="form.name" class="mx-auto h-32 w-32 object-cover rounded-md" />
                      <button
                        type="button"
                        @click="removeImage"
                        class="mt-2 text-sm text-red-600 hover:text-red-500"
                      >
                        Remove Image
                      </button>
                    </div>
                    <svg v-else class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                      <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                    <div class="flex text-sm text-gray-600">
                      <label for="image-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                        <span>Upload a file</span>
                        <input
                          id="image-upload"
                          ref="imageInput"
                          type="file"
                          accept="image/*"
                          @change="handleImageUpload"
                          class="sr-only"
                        />
                      </label>
                      <p class="pl-1">or drag and drop</p>
                    </div>
                    <p class="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                  </div>
                </div>
                <div v-if="uploadProgress" class="mt-2">
                  <div class="bg-gray-200 rounded-full h-2">
                    <div class="bg-primary-600 h-2 rounded-full" :style="{ width: uploadProgress + '%' }"></div>
                  </div>
                  <p class="text-sm text-gray-500 mt-1">Uploading... {{ uploadProgress }}%</p>
                </div>
                <div v-if="errors.image" class="mt-1 text-sm text-red-600">{{ errors.image }}</div>
              </div>

              <!-- Availability -->
              <div class="sm:col-span-2">
                <div class="relative flex items-start">
                  <div class="flex items-center h-5">
                    <input
                      id="is_available"
                      v-model="form.is_available"
                      type="checkbox"
                      class="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                    />
                  </div>
                  <div class="ml-3 text-sm">
                    <label for="is_available" class="font-medium text-gray-700">Available</label>
                    <p class="text-gray-500">This menu item is currently available for ordering.</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Form Error -->
            <div v-if="formError" class="rounded-md bg-red-50 p-4">
              <div class="text-sm text-red-800">{{ formError }}</div>
            </div>

            <!-- Actions -->
            <div class="flex justify-end space-x-3">
              <router-link
                to="/menus"
                class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Cancel
              </router-link>
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                <span v-if="loading">{{ isEdit ? 'Updating...' : 'Creating...' }}</span>
                <span v-else>{{ isEdit ? 'Update Menu' : 'Create Menu' }}</span>
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
import { menuService } from '@/services/menu'

export default {
  name: 'MenuFormView',
  components: {
    Navbar,
    AlertDialog
  },
  data() {
    return {
      user: null,
      isEdit: false,
      menuId: null,
      categories: [],
      customCategory: '',
      form: {
        name: '',
        description: '',
        price: '',
        category: '',
        image_url: '',
        is_available: true
      },
      errors: {},
      formError: '',
      loading: false,
      uploadProgress: null,
      alert: {
        show: false,
        type: 'success',
        title: '',
        message: ''
      }
    }
  },
  async created() {
    await this.loadUser()
    await this.loadCategories()
    
    if (this.$route.params.id) {
      this.isEdit = true
      this.menuId = parseInt(this.$route.params.id)
      await this.loadMenu()
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
    async loadCategories() {
      try {
        this.categories = await menuService.getCategories()
        // Add default categories if empty
        if (this.categories.length === 0) {
          this.categories = ['Main Course', 'Appetizer', 'Dessert', 'Beverage', 'Snack']
        }
      } catch (error) {
        console.error('Failed to load categories:', error)
        this.categories = ['Main Course', 'Appetizer', 'Dessert', 'Beverage', 'Snack']
      }
    },
    async loadMenu() {
      try {
        const menu = await menuService.getMenu(this.menuId)
        this.form = {
          name: menu.name,
          description: menu.description || '',
          price: menu.price,
          category: menu.category,
          image_url: menu.image_url || '',
          is_available: menu.is_available
        }
      } catch (error) {
        this.showAlert('error', 'Error', error.error || 'Failed to load menu')
        this.$router.push('/menus')
      }
    },
    async handleImageUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      // Validate file
      if (!file.type.startsWith('image/')) {
        this.errors.image = 'Please select a valid image file'
        return
      }

      if (file.size > 10 * 1024 * 1024) { // 10MB
        this.errors.image = 'Image size must be less than 10MB'
        return
      }

      this.errors.image = ''
      this.uploadProgress = 0

      try {
        // Simulate upload progress
        const progressInterval = setInterval(() => {
          if (this.uploadProgress < 90) {
            this.uploadProgress += 10
          }
        }, 100)

        const response = await menuService.uploadImage(file)
        
        clearInterval(progressInterval)
        this.uploadProgress = 100
        
        setTimeout(() => {
          this.uploadProgress = null
          this.form.image_url = response.image_url
        }, 500)
      } catch (error) {
        this.uploadProgress = null
        this.errors.image = error.error || 'Failed to upload image'
      }
    },
    removeImage() {
      this.form.image_url = ''
      this.$refs.imageInput.value = ''
    },
    validateForm() {
      this.errors = {}
      this.formError = ''

      if (!this.form.name.trim()) {
        this.errors.name = 'Menu name is required'
      }

      if (!this.form.category) {
        this.errors.category = 'Category is required'
      }

      if (!this.form.price || this.form.price <= 0) {
        this.errors.price = 'Price must be greater than 0'
      }

      if (this.form.category === 'custom' && !this.customCategory.trim()) {
        this.errors.category = 'New category name is required'
      }

      return Object.keys(this.errors).length === 0
    },
    async handleSubmit() {
      if (!this.validateForm()) {
        return
      }

      this.loading = true

      try {
        const menuData = { ...this.form }
        
        // Use custom category if specified
        if (menuData.category === 'custom') {
          menuData.category = this.customCategory.trim()
        }

        if (this.isEdit) {
          await menuService.updateMenu(this.menuId, menuData)
          this.showAlert('success', 'Success', 'Menu updated successfully')
        } else {
          await menuService.createMenu(menuData)
          this.showAlert('success', 'Success', 'Menu created successfully')
        }

        setTimeout(() => {
          this.$router.push('/menus')
        }, 1500)
      } catch (error) {
        this.formError = error.error || `Failed to ${this.isEdit ? 'update' : 'create'} menu`
        
        // Handle validation errors
        if (error.details && typeof error.details === 'object') {
          this.errors = error.details
        }
      } finally {
        this.loading = false
      }
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