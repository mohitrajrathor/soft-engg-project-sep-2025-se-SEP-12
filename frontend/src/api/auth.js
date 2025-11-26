/**
 * Authentication API endpoints
 */

import api from './axios'

export const authAPI = {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @param {string} userData.email - User email
   * @param {string} userData.password - User password
   * @param {string} userData.role - User role (student, ta, instructor, admin)
   * @param {string} [userData.full_name] - User full name
   * @returns {Promise} Response with tokens and user data
   */
  async register(userData) {
    const response = await api.post('/auth/signup', userData)
    return response.data
  },

  /**
   * Login user
   * @param {Object} credentials - Login credentials
   * @param {string} credentials.email - User email
   * @param {string} credentials.password - User password
   * @returns {Promise} Response with tokens and user data
   */
  async login(credentials) {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  /**
   * Refresh access token
   * @param {string} refreshToken - Refresh token
   * @returns {Promise} Response with new tokens
   */
  async refreshToken(refreshToken) {
    const response = await api.post('/auth/refresh', {
      refresh_token: refreshToken
    })
    return response.data
  },

  /**
   * Get current user profile
   * @returns {Promise} Current user data
   */
  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  /**
   * Update current user profile
   * @param {Object} updates - Profile updates
   * @returns {Promise} Updated user data
   */
  async updateProfile(updates) {
    const response = await api.put('/auth/me', updates)
    return response.data
  },

  /**
   * Logout (client-side only - clear tokens)
   */
  logout() {
    // Backend is stateless (JWT), so just clear local tokens
    return Promise.resolve()
  }
}
