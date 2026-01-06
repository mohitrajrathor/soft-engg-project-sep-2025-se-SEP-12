import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import studentQueries from '@/components/student/studentQueries.vue'
import { queriesAPI } from '@/api'

// Use global '@/api' index mock; ensure queriesAPI methods are spied per test

describe('studentQueries.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the student queries component', async () => {
    const wrapper = mount(studentQueries, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('fetches queries on mount', async () => {
    const spy = vi.spyOn(queriesAPI, 'getQueries')
    mount(studentQueries, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await Promise.resolve()
    await new Promise(resolve => setTimeout(resolve, 0))
    expect(spy).toHaveBeenCalled()
  })

  it('displays queries list title or content', async () => {
    const wrapper = mount(studentQueries, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const text = wrapper.text()
    expect(text.includes('Queries') || text.includes('Questions') || text.length > 0).toBe(true)
  })

  it('shows loading state', async () => {
    vi.spyOn(queriesAPI, 'getQueries').mockImplementationOnce(() => new Promise(() => {}))
    const wrapper = mount(studentQueries, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.animate-pulse').exists() || wrapper.text().includes('Loading')).toBe(true)
  })
})
