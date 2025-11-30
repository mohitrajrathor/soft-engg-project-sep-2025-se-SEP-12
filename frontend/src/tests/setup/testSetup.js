import { config } from '@vue/test-utils'
import { vi } from 'vitest'
import { createPinia } from 'pinia'

// Mock vue-router globally
vi.mock('vue-router', () => ({
  useRoute: vi.fn(() => ({
    params: {},
    query: {},
    path: '/',
  })),
  useRouter: vi.fn(() => ({
    push: vi.fn(),
    replace: vi.fn(),
    go: vi.fn(),
    back: vi.fn(),
  })),
  RouterLink: {
    name: 'RouterLink',
    template: '<a><slot /></a>',
  },
  RouterView: {
    name: 'RouterView',
    template: '<div><slot /></div>',
  },
}))

// Mock Chart.js to avoid canvas issues
vi.mock('chart.js', () => ({
  Chart: class Chart {
    constructor() {
      this.destroy = vi.fn()
      this.update = vi.fn()
      this.render = vi.fn()
    }
    static register() {}
  },
  registerables: [],
  Title: {},
  Tooltip: {},
  Legend: {},
  LineElement: {},
  PointElement: {},
  CategoryScale: {},
  LinearScale: {},
  BarElement: {},
  ArcElement: {},
}))

// Mock theme and user stores
vi.mock('@/stores/theme', () => ({
  useThemeStore: vi.fn(() => ({
    isDarkMode: false,
    toggleTheme: vi.fn(),
  })),
}))

vi.mock('@/stores/user', () => ({
  useUserStore: vi.fn(() => ({
    user: {
      id: 1,
      name: 'Test User',
      email: 'test@example.com',
      role: 'student',
    },
    isAuthenticated: true,
    login: vi.fn(),
    logout: vi.fn(),
  })),
}))

// Mock API modules
// Aggregate API index used in components (e.g., queriesAPI, analyticsAPI)
vi.mock('@/api', () => ({
  queriesAPI: {
    getQueries: vi.fn(async () => ({ queries: [] })),
    getQuery: vi.fn(async (id) => ({ id, title: 'Mock Query', status: 'OPEN', description: '...' })),
    addResponse: vi.fn(async () => ({ success: true })),
    getStatistics: vi.fn(async () => ({ counts: {}, trends: [] })),
  },
  analyticsAPI: {
    getAllAnalytics: vi.fn(async () => ({ charts: [], stats: {} })),
  },
  dashboardAPI: {
    getStudentDashboard: vi.fn(async () => ({ stats: {} })),
    getInstructorDashboard: vi.fn(async () => ({ stats: {} })),
    getAdminDashboard: vi.fn(async () => ({ stats: {} })),
    getTADashboard: vi.fn(async () => ({ stats: {} })),
  },
  chatbotAPI: {
    getChatbotStatus: vi.fn(async () => ({ available: true })),
  },
  api: {
    // generic export some components may reference
    fetchProfile: vi.fn(async () => ({ name: 'TA Test', email: 'ta@example.com' })),
  },
}))
vi.mock('@/api/dashboard', () => ({
  default: {
    getStudentDashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
    getTADashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
    getInstructorDashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
    getAdminDashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
  },
  getStudentDashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
  getTADashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
  getInstructorDashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
  getAdminDashboard: vi.fn(() => Promise.resolve({ data: { stats: {} } })),
}))

vi.mock('@/api/queries', () => ({
  default: {
    getQueries: vi.fn(() => Promise.resolve({ data: [] })),
    getStudentQueries: vi.fn(() => Promise.resolve({ data: [] })),
    getUnresolvedQueries: vi.fn(() => Promise.resolve({ data: [] })),
    createQuery: vi.fn(() => Promise.resolve({ data: {} })),
  },
  getQueries: vi.fn(() => Promise.resolve({ data: [] })),
  getStudentQueries: vi.fn(() => Promise.resolve({ data: [] })),
  getUnresolvedQueries: vi.fn(() => Promise.resolve({ data: [] })),
  createQuery: vi.fn(() => Promise.resolve({ data: {} })),
}))

vi.mock('@/api/analytics', () => ({
  default: {
    getAnalytics: vi.fn(() => Promise.resolve({ data: {} })),
    getDiscussionSummaries: vi.fn(() => Promise.resolve({ data: [] })),
  },
  getAnalytics: vi.fn(() => Promise.resolve({ data: {} })),
  getDiscussionSummaries: vi.fn(() => Promise.resolve({ data: [] })),
}))

vi.mock('@/api/doubts', () => ({
  default: {
    getDoubts: vi.fn(() => Promise.resolve({ data: [] })),
    getDoubtSummary: vi.fn(() => Promise.resolve({ data: {} })),
  },
  getDoubts: vi.fn(() => Promise.resolve({ data: [] })),
  getDoubtSummary: vi.fn(() => Promise.resolve({ data: {} })),
}))

vi.mock('@/api/instructorAnalytics', () => ({
  default: {
    getDiscussionSummaries: vi.fn(() => Promise.resolve({ data: [] })),
  },
  getDiscussionSummaries: vi.fn(() => Promise.resolve({ data: [] })),
}))

// Mock canvas element's getContext
HTMLCanvasElement.prototype.getContext = vi.fn(() => ({
  fillRect: vi.fn(),
  clearRect: vi.fn(),
  getImageData: vi.fn(() => ({ data: [] })),
  putImageData: vi.fn(),
  createImageData: vi.fn(() => []),
  setTransform: vi.fn(),
  drawImage: vi.fn(),
  save: vi.fn(),
  fillText: vi.fn(),
  restore: vi.fn(),
  beginPath: vi.fn(),
  moveTo: vi.fn(),
  lineTo: vi.fn(),
  closePath: vi.fn(),
  stroke: vi.fn(),
  translate: vi.fn(),
  scale: vi.fn(),
  rotate: vi.fn(),
  arc: vi.fn(),
  fill: vi.fn(),
  measureText: vi.fn(() => ({ width: 0 })),
  transform: vi.fn(),
  rect: vi.fn(),
  clip: vi.fn(),
}))

// Create a new pinia instance for each test
const pinia = createPinia()

// Provide Pinia globally to all test components
config.global.plugins = [pinia]

// Globally stub Vue components
config.global.stubs = {
  FontAwesomeIcon: true,
  RouterLink: true,
  RouterView: true,
}
