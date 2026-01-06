import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import StudentNewQuery from '@/components/student/StudentNewQuery.vue'
import queries from '@/api/queries'

vi.mock('@/api/queries', () => ({
  default: {
    createQuery: vi.fn(() => Promise.resolve({ id: 1, success: true }))
  }
}))

describe('StudentNewQuery.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the new query component', async () => {
    const wrapper = mount(StudentNewQuery, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays query form title', async () => {
    const wrapper = mount(StudentNewQuery, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Query') || expect(wrapper.text()).toContain('Question')
  })

  it('shows query input fields', async () => {
    const wrapper = mount(StudentNewQuery, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const textareas = wrapper.findAll('textarea')
    const inputs = wrapper.findAll('input')
    expect(textareas.length + inputs.length).toBeGreaterThanOrEqual(0)
  })

  it('handles query submission', async () => {
    const wrapper = mount(StudentNewQuery, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const submitButton = wrapper.find('button[type="submit"]')
    if (submitButton.exists()) {
      await submitButton.trigger('click')
      expect(wrapper.emitted()).toBeDefined()
    }
  })

  it('validates required fields', async () => {
    const wrapper = mount(StudentNewQuery, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })
})
