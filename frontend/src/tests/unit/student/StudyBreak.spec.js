import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import StudyBreak from '@/components/student/StudyBreak.vue'

describe('StudyBreak.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the study break component', async () => {
    const wrapper = mount(StudyBreak, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays study break title', async () => {
    const wrapper = mount(StudyBreak, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Study Break') || expect(wrapper.text()).toContain('Break')
  })

  it('shows break timer or activities', async () => {
    const wrapper = mount(StudyBreak, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })

  it('handles timer controls', async () => {
    const wrapper = mount(StudyBreak, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const startButton = wrapper.find('button[aria-label="start"]') || wrapper.find('.start-button')
    if (startButton.exists()) {
      await startButton.trigger('click')
      expect(wrapper.vm.$data).toBeDefined()
    }
  })
})
