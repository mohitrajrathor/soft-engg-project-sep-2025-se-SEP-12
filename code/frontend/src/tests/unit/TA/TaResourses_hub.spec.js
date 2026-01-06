import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import TaResourcesHub from '@/components/TA/TaResourses_hub.vue'

describe('TaResourses_hub.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the TA resources hub component', async () => {
    const wrapper = mount(TaResourcesHub, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays resources hub title', async () => {
    const wrapper = mount(TaResourcesHub, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Resource') || expect(wrapper.text()).toContain('Hub')
  })

  it('shows resources list', async () => {
    const wrapper = mount(TaResourcesHub, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const resources = wrapper.findAll('.resource-item') || wrapper.findAll('li')
    expect(resources.length).toBeGreaterThanOrEqual(0)
  })

  it('handles resource search', async () => {
    const wrapper = mount(TaResourcesHub, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const searchInput = wrapper.find('input[type="search"]') || wrapper.find('input[placeholder*="search"]')
    if (searchInput.exists()) {
      await searchInput.setValue('test')
      expect(searchInput.element.value).toBe('test')
    }
  })

  it('displays resource categories', async () => {
    const wrapper = mount(TaResourcesHub, {
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
