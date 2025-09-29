import api from './api'

class MenuService {
  async getMenus(params = {}) {
    try {
      const response = await api.get('/menus', { params })
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch menus' }
    }
  }

  async getMenu(id) {
    try {
      const response = await api.get(`/menus/${id}`)
      return response.data.menu
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch menu' }
    }
  }

  async createMenu(menuData) {
    try {
      const response = await api.post('/menus', menuData)
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to create menu' }
    }
  }

  async updateMenu(id, menuData) {
    try {
      const response = await api.put(`/menus/${id}`, menuData)
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to update menu' }
    }
  }

  async deleteMenu(id) {
    try {
      const response = await api.delete(`/menus/${id}`)
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to delete menu' }
    }
  }

  async getCategories() {
    try {
      const response = await api.get('/menus/categories')
      return response.data.categories
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch categories' }
    }
  }

  async uploadImage(file) {
    try {
      const formData = new FormData()
      formData.append('image', file)
      
      const response = await api.post('/menus/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      throw error.response?.data || { error: 'Failed to upload image' }
    }
  }
}

export const menuService = new MenuService()