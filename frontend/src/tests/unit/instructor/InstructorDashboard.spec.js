import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import InstructorDashboard from '@/components/instructor/InstructorDashboard.vue'

describe('InstructorDashboard.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the instructor dashboard component', async () => {
    const wrapper = mount(InstructorDashboard, {
      global: {
        stubs: {
          InstructorSidebar: true,
          ChartComponent: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays dashboard title or greeting', async () => {
    const wrapper = mount(InstructorDashboard, {
      global: {
        stubs: {
          InstructorSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const text = wrapper.text()
    expect(text.includes('Dashboard') || text.includes('Welcome back')).toBe(true)
  })
  
  // Component is static; ensure content renders without API dependency
  it('renders content without API calls', async () => {
    const wrapper = mount(InstructorDashboard, {
      global: {
        stubs: {
          InstructorSidebar: true,
          ChartComponent: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text().length > 0).toBe(true)
  })
})
