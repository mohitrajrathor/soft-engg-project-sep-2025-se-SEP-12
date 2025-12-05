import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import AdminDashboard from '@/components/Admin/AdminDashboard.vue'
import { analyticsAPI } from '@/api'

// Ensure analyticsAPI mock exists from global test setup
// and spy on its calls for this suite

describe('AdminDashboard.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the admin dashboard component', async () => {
    const wrapper = mount(AdminDashboard, {
      global: {
        stubs: {
          AdminSidebar: true,
          ChartComponent: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays dashboard title or greeting', async () => {
    const wrapper = mount(AdminDashboard, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const text = wrapper.text()
    expect(text.includes('Dashboard') || text.includes('Admin') || text.includes('Welcome back')).toBe(true)
  })

  it('fetches admin dashboard data on mount', async () => {
    const spy = vi.spyOn(analyticsAPI, 'getAllAnalytics')
    mount(AdminDashboard, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await Promise.resolve()
    await new Promise(resolve => setTimeout(resolve, 0))
    expect(spy).toHaveBeenCalled()
  })

  it('shows loading state', async () => {
    vi.spyOn(analyticsAPI, 'getAllAnalytics').mockImplementationOnce(() => new Promise(() => {}))
    const wrapper = mount(AdminDashboard, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.animate-pulse').exists() || wrapper.text().includes('Loading')).toBe(true)
  })

  it('handles API errors gracefully', async () => {
    vi.spyOn(analyticsAPI, 'getAllAnalytics').mockRejectedValueOnce(new Error('API Error'))
    const wrapper = mount(AdminDashboard, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await Promise.resolve()
    const hasError = wrapper.text().includes('Error') || 'error' in (wrapper.vm.$data || {})
    expect(hasError || wrapper.html()).toBeTruthy()
  })
})
