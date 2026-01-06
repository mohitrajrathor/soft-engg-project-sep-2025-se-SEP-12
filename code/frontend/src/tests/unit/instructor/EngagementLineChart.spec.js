import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import EngagementLineChart from '@/components/instructor/EngagementLineChart.vue'

describe('EngagementLineChart.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the engagement line chart component', async () => {
    const wrapper = mount(EngagementLineChart, {
      props: {
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
          datasets: [{
            label: 'Engagement',
            data: [65, 59, 80, 81, 56]
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

  it('renders with internal chartData', async () => {
    const wrapper = mount(EngagementLineChart, {
      global: { stubs: { Line: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders chart container', async () => {
    const wrapper = mount(EngagementLineChart, {
      global: { stubs: { Line: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })
})
