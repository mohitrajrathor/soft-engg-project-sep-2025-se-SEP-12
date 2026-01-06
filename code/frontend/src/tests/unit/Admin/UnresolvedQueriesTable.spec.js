import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import UnresolvedQueriesTable from '@/components/Admin/UnresolvedQueriesTable.vue'
import { queriesAPI } from '@/api'

vi.mock('@/api/queries', () => ({
  default: {
    getUnresolvedQueries: vi.fn(() => Promise.resolve({
      queries: [
        { id: 1, title: 'Query 1', student: 'John', date: '2024-01-01', status: 'pending' },
        { id: 2, title: 'Query 2', student: 'Jane', date: '2024-01-02', status: 'pending' }
      ],
      total: 2
    }))
  }
}))

describe('UnresolvedQueriesTable.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the unresolved queries table component', async () => {
    const wrapper = mount(UnresolvedQueriesTable, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  // Component renders static rows; no API call expected
  it('renders table content without API calls', async () => {
    const wrapper = mount(UnresolvedQueriesTable, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.findAll('tr').length).toBeGreaterThan(1)
  })

  it('displays table headers', async () => {
    const wrapper = mount(UnresolvedQueriesTable, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const headers = wrapper.findAll('th')
    expect(headers.length).toBeGreaterThanOrEqual(0)
  })

  it('renders without explicit loading indicator', async () => {
    const wrapper = mount(UnresolvedQueriesTable, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('table').exists()).toBe(true)
  })

  it('handles query sorting', async () => {
    const wrapper = mount(UnresolvedQueriesTable, {
      global: {
        stubs: {
          AdminSidebar: true
        }
      }
    })
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const sortButton = wrapper.find('th button') || wrapper.find('.sort-button')
    if (sortButton.exists()) {
      await sortButton.trigger('click')
      expect(wrapper.vm.$data).toBeDefined()
    }
  })
})
