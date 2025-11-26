import AdminDashboard from '../components/Admin/AdminDashboard.vue'

export default {
  path: '/admin',
  children: [
    { path: '', redirect: '/admin/dashboard' },
    { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboard }
  ],
}
