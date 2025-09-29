import api from './api'

class OrderService {
  async getOrders(params = {}) {
    try {
      const response = await api.get('/orders', { params })
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch orders' }
    }
  }

  async getOrder(id) {
    try {
      const response = await api.get(`/orders/${id}`)
      return response.data.order
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch order' }
    }
  }

  async createOrder(orderData) {
    try {
      const response = await api.post('/orders', orderData)
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to create order' }
    }
  }

  async updateOrder(id, orderData) {
    try {
      const response = await api.put(`/orders/${id}`, orderData)
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to update order' }
    }
  }

  async updateOrderStatus(id, status) {
    try {
      const response = await api.put(`/orders/${id}/status`, { status })
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to update order status' }
    }
  }

  async deleteOrder(id) {
    try {
      const response = await api.delete(`/orders/${id}`)
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to delete order' }
    }
  }

  async exportOrdersPDF(params = {}) {
    try {
      const response = await api.get('/orders/export-pdf', { 
        params,
        responseType: 'blob' // Important for file downloads
      })
      
      // Create blob URL and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      
      // Create temporary download link
      const link = document.createElement('a')
      link.href = url
      
      // Generate filename based on current date and filter
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0]
      const statusFilter = params.status ? `_${params.status}` : '_all'
      link.download = `orders${statusFilter}_${timestamp}.pdf`
      
      // Trigger download
      document.body.appendChild(link)
      link.click()
      
      // Cleanup
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      return { success: true, message: 'PDF exported successfully' }
    } catch (error) {
      throw error.response?.data || { error: 'Failed to export orders PDF' }
    }
  }

  async exportSingleOrderPDF(id) {
    try {
      const response = await api.get(`/orders/${id}/export-pdf`, {
        responseType: 'blob' // Important for file downloads
      })
      
      // Create blob URL and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      
      // Create temporary download link
      const link = document.createElement('a')
      link.href = url
      
      // Generate filename
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0]
      link.download = `order_${id}_${timestamp}.pdf`
      
      // Trigger download
      document.body.appendChild(link)
      link.click()
      
      // Cleanup
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      return { success: true, message: 'Order PDF exported successfully' }
    } catch (error) {
      throw error.response?.data || { error: 'Failed to export order PDF' }
    }
  }
}

export const orderService = new OrderService()