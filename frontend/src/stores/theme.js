// src/stores/theme.js
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // State
  const currentTheme = ref(localStorage.getItem('theme') || 'light')

  // Watch for theme changes and save to localStorage
  watch(
    () => currentTheme.value,
    (newTheme) => {
      localStorage.setItem('theme', newTheme)
      applyTheme(newTheme)
    }
  )

  // Initialize theme on app load
  const initTheme = () => {
    const savedTheme = localStorage.getItem('theme') || 'light'
    currentTheme.value = savedTheme
    applyTheme(savedTheme)
  }

  // Apply theme to document
  const applyTheme = (theme) => {
    const root = document.documentElement
    root.setAttribute('data-theme', theme)
  }

  // Toggle theme
  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light'
  }

  // Set specific theme
  const setTheme = (theme) => {
    if (['light', 'dark'].includes(theme)) {
      currentTheme.value = theme
    }
  }

  return {
    currentTheme,
    initTheme,
    toggleTheme,
    setTheme
  }
})
