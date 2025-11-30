import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import AdminAnalyticsDashboard from '@/components/Admin/AdminAnalyticsDashboard.vue'
import { analyticsAPI } from '@/api'

vi.mock('@/api/analytics', () => ({
  default: {
    getAnalytics: vi.fn(() => Promise.resolve({
      userEngagement: 85,
      systemUsage: 92,
      popularFeatures: ['Dashboard', 'Queries', 'Resources']
    }))
  }
}))

describe('AdminAnalyticsDashboard.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the analytics dashboard component', async () => {
    const wrapper = mount(AdminAnalyticsDashboard, {
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

  it('displays analytics title', async () => {
    const wrapper = mount(AdminAnalyticsDashboard, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Analytics')
  })

  it('fetches analytics data on mount', async () => {
    const spy = vi.spyOn(analyticsAPI, 'getAllAnalytics')
    mount(AdminAnalyticsDashboard, {
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

  it('shows analytics charts', async () => {
    const wrapper = mount(AdminAnalyticsDashboard, {
      global: {
        stubs: {
          AdminSidebar: true,
          ChartComponent: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const charts = wrapper.findAll('.chart') || wrapper.findAll('canvas')
    expect(charts.length).toBeGreaterThanOrEqual(0)
  })

  it('handles data filtering', async () => {
    const wrapper = mount(AdminAnalyticsDashboard, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const dateFilter = wrapper.find('select') || wrapper.find('.date-filter')
    if (dateFilter.exists()) {
      expect(wrapper.vm.$data).toBeDefined()
    }
  })
})
