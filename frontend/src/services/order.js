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
}

export const orderService = new OrderService()