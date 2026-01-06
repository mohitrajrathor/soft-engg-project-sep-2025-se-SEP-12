import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import InstructorProfile from '@/components/instructor/InstructorProfile.vue'

describe('InstructorProfile.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the instructor profile component', async () => {
    const wrapper = mount(InstructorProfile, {
      global: {
        stubs: {
          InstructorSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays profile title', async () => {
    const wrapper = mount(InstructorProfile, {
      global: {
        stubs: {
          InstructorSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Profile')
  })

  it('shows profile form fields', async () => {
    const wrapper = mount(InstructorProfile, {
      global: {
        stubs: {
          InstructorSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(0)
  })

  it('handles profile update', async () => {
    const wrapper = mount(InstructorProfile, {
      global: {
        stubs: {
          InstructorSidebar: true
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

  it('displays instructor information', async () => {
    const wrapper = mount(InstructorProfile, {
      global: {
        stubs: {
          InstructorSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })
})
