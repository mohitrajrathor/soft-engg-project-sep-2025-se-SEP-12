import { createRouter, createWebHistory } from 'vue-router'

// Auth / landing
import LandingPage from '../components/LandingPage.vue'
import RegisterPage from '../components/auth/RegisterPage.vue'
import LoginPage from '../components/auth/LoginPage.vue'

// Role-based route imports
import studentRoutes from './studentRoutes'
import instructorRoutes from './instructorRoutes'
import taRoutes from './TaRoutes'
import adminRoutes from './adminRoutes';

const routes = [
  { path: '/', component: LandingPage },
  { path: '/register', component: RegisterPage },
  { path: '/login', component: LoginPage },
  {
    path: '/student',
    children: [
      { path: '', redirect: '/student/dashboard' },
      ...studentRoutes
    ],
  },

  {
    path: '/ta',
    children: [
     { path: '', redirect: '/ta/dashboard' },
      ...taRoutes
    ],
  },
  instructorRoutes,
  adminRoutes,
  
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
