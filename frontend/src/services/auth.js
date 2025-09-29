import api from './api'

class AuthService {
  async login(username, password) {
    try {
      const response = await api.post('/auth/login', { username, password })
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Login failed' }
    }
  }

  async logout() {
    try {
      const response = await api.post('/auth/logout')
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Logout failed' }
    }
  }

  async checkAuth() {
    try {
      const response = await api.get('/auth/status')
      return response.data.authenticated
    } catch (error) {
      return false
    }
  }

  async getCurrentUser() {
    try {
      const response = await api.get('/auth/me')
      return response.data.user
    } catch (error) {
      throw error.response?.data || { error: 'Failed to get user info' }
    }
  }
}

export const authService = new AuthService()