/// <reference types="vitest" />
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',              // simulate browser environment
    globals: true,                     // allows global test functions (describe, it, etc.)
    setupFiles: './src/tests/setup/testSetup.js',
    include: ['src/**/*.{test,spec}.{js,ts,vue}'],
    coverage: {
      reporter: ['text', 'json', 'html'], // optional coverage report
    },
  },
})
