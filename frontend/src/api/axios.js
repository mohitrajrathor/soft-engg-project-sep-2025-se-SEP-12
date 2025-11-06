/**
 * Axios instance configured for AURA backend API
 */

import axios from 'axios'
import { useUserStore } from '@/stores/user'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
})

// Request interceptor - Add JWT token to requests
api.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    const token = userStore.token

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle token expiration
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // If token expired (401) and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const userStore = useUserStore()
        const refreshToken = userStore.refreshToken

        if (refreshToken) {
          // Try to refresh the token
          const response = await axios.post('http://localhost:8000/api/auth/refresh', {
            refresh_token: refreshToken
          })

          const { access_token, refresh_token: newRefreshToken } = response.data

          // Update tokens
          userStore.setTokens(access_token, newRefreshToken)

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        const userStore = useUserStore()
        userStore.clearUser()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api
