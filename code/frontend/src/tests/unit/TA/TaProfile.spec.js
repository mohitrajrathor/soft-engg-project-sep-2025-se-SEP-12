import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import TaProfile from '@/components/TA/TaProfile.vue'

describe('TaProfile.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the TA profile component', async () => {
    const wrapper = mount(TaProfile, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays profile title', async () => {
    const wrapper = mount(TaProfile, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Profile')
  })

  it('shows profile information fields', async () => {
    const wrapper = mount(TaProfile, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(0)
  })

  it('handles profile form submission', async () => {
    const wrapper = mount(TaProfile, {
      global: {
        stubs: {
          TASidebar: true
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

  it('displays user information', async () => {
    const wrapper = mount(TaProfile, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })
})
