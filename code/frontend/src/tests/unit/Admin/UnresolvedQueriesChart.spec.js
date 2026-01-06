import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import UnresolvedQueriesChart from '@/components/Admin/UnresolvedQueriesChart.vue'

describe('UnresolvedQueriesChart.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the unresolved queries chart component', async () => {
    const wrapper = mount(UnresolvedQueriesChart, {
      props: {
        data: {
          labels: ['Week 1', 'Week 2', 'Week 3'],
          datasets: [{
            label: 'Unresolved',
            data: [10, 15, 8]
          }]
        }
      },
      global: {
        stubs: {
          Line: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders using internal data without props', async () => {
    const wrapper = mount(UnresolvedQueriesChart, {
      global: { stubs: { Pie: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders chart container', async () => {
    const wrapper = mount(UnresolvedQueriesChart, {
      global: { stubs: { Pie: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })

  it('renders chart with trend data', async () => {
    const wrapper = mount(UnresolvedQueriesChart, {
      props: {
        data: {
          labels: ['Day 1', 'Day 2'],
          datasets: [{ data: [20, 15] }]
        }
      },
      global: {
        stubs: { Line: true }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })
})
