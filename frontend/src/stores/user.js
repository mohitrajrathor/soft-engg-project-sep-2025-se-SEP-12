// src/stores/user.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null,
    role: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.role === 'admin',
  },

  actions: {
    setUser(token, role) {
      this.token = token
      this.role = role
    },
    clearUser() {
      this.token = null
      this.role = null
    },
  },
})
