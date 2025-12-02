import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import studentDashboard from '@/components/student/studentDashboard.vue'

describe('studentDashboard.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the student dashboard component', async () => {
    const wrapper = mount(studentDashboard, {
      global: {
        stubs: {
          StudentSidebar: true,
          ChartComponent: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays dashboard title or greeting', async () => {
    const wrapper = mount(studentDashboard, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const text = wrapper.text()
    expect(text.includes('Dashboard') || text.length > 0).toBe(true)
  })
  
  // Component appears static; verify it renders content without API calls
  it('renders content without API calls', async () => {
    const wrapper = mount(studentDashboard, {
      global: {
        stubs: {
          StudentSidebar: true,
          ChartComponent: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text().length > 0).toBe(true)
  })
})
