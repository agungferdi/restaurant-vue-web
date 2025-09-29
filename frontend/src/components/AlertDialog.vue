<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" v-if="show">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 transition-opacity">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-sm sm:w-full sm:p-6">
        <div>
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full" :class="typeClasses.bg">
            <component :is="icon" class="h-6 w-6" :class="typeClasses.text" />
          </div>
          <div class="mt-3 text-center sm:mt-5">
            <h3 class="text-lg leading-6 font-medium text-gray-900">{{ title }}</h3>
            <div class="mt-2">
              <p class="text-sm text-gray-500">{{ message }}</p>
            </div>
          </div>
        </div>
        <div class="mt-5 sm:mt-6">
          <button
            type="button"
            @click="close"
            class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 sm:text-sm"
            :class="typeClasses.button"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertDialog',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'success',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      default: ''
    }
  },
  emits: ['close'],
  computed: {
    typeClasses() {
      const classes = {
        success: {
          bg: 'bg-green-100',
          text: 'text-green-600',
          button: 'bg-green-600 hover:bg-green-700 focus:ring-green-500'
        },
        error: {
          bg: 'bg-red-100',
          text: 'text-red-600',
          button: 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
        },
        warning: {
          bg: 'bg-yellow-100',
          text: 'text-yellow-600',
          button: 'bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500'
        },
        info: {
          bg: 'bg-blue-100',
          text: 'text-blue-600',
          button: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
        }
      }
      return classes[this.type]
    },
    icon() {
      const icons = {
        success: 'CheckCircleIcon',
        error: 'ExclamationTriangleIcon',
        warning: 'ExclamationTriangleIcon',
        info: 'InformationCircleIcon'
      }
      return icons[this.type]
    }
  },
  methods: {
    close() {
      this.$emit('close')
    }
  }
}
</script>

<script setup>
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  InformationCircleIcon 
} from '@heroicons/vue/24/outline'
</script>