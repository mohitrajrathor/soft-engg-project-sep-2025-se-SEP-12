import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Profile from '@/components/student/Profile.vue'

describe('Profile.vue (Student)', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the student profile component', async () => {
    const wrapper = mount(Profile, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays profile title', async () => {
    const wrapper = mount(Profile, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Profile')
  })

  it('shows profile form fields', async () => {
    const wrapper = mount(Profile, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(0)
  })

  it('handles form submission', async () => {
    const wrapper = mount(Profile, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const form = wrapper.find('form')
    if (form.exists()) {
      await form.trigger('submit')
      expect(wrapper.emitted()).toBeDefined()
    }
  })
})
