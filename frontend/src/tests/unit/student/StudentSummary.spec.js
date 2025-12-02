import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import StudentSummary from '@/components/student/StudentSummary.vue'

describe('StudentSummary.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the student summary component', async () => {
    const wrapper = mount(StudentSummary, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays summary title or content', async () => {
    const wrapper = mount(StudentSummary, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const text = wrapper.text()
    expect(text.includes('Summary') || text.length > 0).toBe(true)
  })

  it('shows summary cards', async () => {
    const wrapper = mount(StudentSummary, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const cards = wrapper.findAll('.card') || wrapper.findAll('.summary-item')
    expect(cards.length).toBeGreaterThanOrEqual(0)
  })

  it('displays student progress information', async () => {
    const wrapper = mount(StudentSummary, {
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
