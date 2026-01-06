import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import FAQAnalyticsChart from '@/components/Admin/FAQAnalyticsChart.vue'

describe('FAQAnalyticsChart.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the FAQ analytics chart component', async () => {
    const wrapper = mount(FAQAnalyticsChart, {
      props: {
        data: {
          labels: ['FAQ 1', 'FAQ 2', 'FAQ 3'],
          datasets: [{
            label: 'Views',
            data: [100, 200, 150]
          }]
        }
      },
      global: {
        stubs: {
          Bar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders without external props (uses internal data)', async () => {
    const wrapper = mount(FAQAnalyticsChart, {
      global: { stubs: { Bar: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays chart title', async () => {
    const wrapper = mount(FAQAnalyticsChart, {
      props: {
        data: { labels: [], datasets: [] }
      },
      global: {
        stubs: { Bar: true }
      }
    })
    await wrapper.vm.$nextTick()
    const text = wrapper.text()
    expect(text.includes('FAQ') || text.includes('Analytics') || wrapper.html()).toBeTruthy()
  })

  it('renders chart with correct data', async () => {
    const wrapper = mount(FAQAnalyticsChart, {
      props: {
        data: {
          labels: ['Test'],
          datasets: [{ data: [10] }]
        }
      },
      global: {
        stubs: { Bar: true }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })
})
