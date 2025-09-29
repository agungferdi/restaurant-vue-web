<template>
  <nav class="bg-primary-600 shadow-lg">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-white rounded-full flex items-center justify-center">
              <span class="text-primary-600 font-bold text-lg">R</span>
            </div>
            <span class="text-white font-bold text-xl">Restaurant Admin</span>
          </router-link>
        </div>
        
        <div class="flex items-center space-x-4">
          <router-link
            to="/"
            class="text-white hover:text-primary-200 px-3 py-2 rounded-md text-sm font-medium"
            :class="{ 'bg-primary-700': $route.name === 'Dashboard' }"
          >
            Dashboard
          </router-link>
          <router-link
            to="/menus"
            class="text-white hover:text-primary-200 px-3 py-2 rounded-md text-sm font-medium"
            :class="{ 'bg-primary-700': $route.path.startsWith('/menus') }"
          >
            Menus
          </router-link>
          <router-link
            to="/orders"
            class="text-white hover:text-primary-200 px-3 py-2 rounded-md text-sm font-medium"
            :class="{ 'bg-primary-700': $route.path.startsWith('/orders') }"
          >
            Orders
          </router-link>
          
          <div class="flex items-center space-x-2 ml-4 pl-4 border-l border-primary-500">
            <span class="text-primary-200 text-sm">{{ user?.username }}</span>
            <button
              @click="handleLogout"
              class="text-white hover:text-primary-200 px-3 py-2 rounded-md text-sm font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { authService } from '@/services/auth'

export default {
  name: 'Navbar',
  props: {
    user: {
      type: Object,
      default: null
    }
  },
  emits: ['logout'],
  methods: {
    async handleLogout() {
      try {
        await authService.logout()
        this.$emit('logout')
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout failed:', error)
      }
    }
  }
}
</script>