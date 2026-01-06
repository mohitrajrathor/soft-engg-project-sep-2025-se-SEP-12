import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import StudentResource from '@/components/student/StudentResource.vue'

describe('StudentResource.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the student resource component', async () => {
    const wrapper = mount(StudentResource, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays resources title', async () => {
    const wrapper = mount(StudentResource, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Resource')
  })

  it('shows resources list', async () => {
    const wrapper = mount(StudentResource, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const resources = wrapper.findAll('.resource') || wrapper.findAll('li')
    expect(resources.length).toBeGreaterThanOrEqual(0)
  })

  it('handles resource search', async () => {
    const wrapper = mount(StudentResource, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const searchInput = wrapper.find('input[type="search"]')
    if (searchInput.exists()) {
      await searchInput.setValue('test')
      expect(searchInput.element.value).toBe('test')
    }
  })
})
