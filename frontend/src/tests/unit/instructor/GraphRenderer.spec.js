import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import GraphRenderer from '@/components/instructor/GraphRenderer.vue'

describe('GraphRenderer.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the graph renderer component', async () => {
    const wrapper = mount(GraphRenderer, {
      props: {
        graphType: 'bar',
        data: {
          labels: ['A', 'B', 'C'],
          datasets: [{ data: [10, 20, 30] }]
        }
      },
      global: {
        stubs: {
          Bar: true,
          Line: true,
          Pie: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('accepts graphData prop with type', async () => {
    const wrapper = mount(GraphRenderer, {
      props: {
        graphData: { type: 'line', labels: [], datasets: [] }
      },
      global: { stubs: { Line: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.$props.graphData.type).toBe('line')
  })

  it('accepts graphData labels and datasets', async () => {
    const graphData = {
      type: 'bar',
      title: 'Test',
      labels: ['X', 'Y', 'Z'],
      datasets: [{ label: 'Test', data: [5, 10, 15] }]
    }
    const wrapper = mount(GraphRenderer, {
      props: { graphData },
      global: { stubs: { Bar: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.$props.graphData.labels).toEqual(graphData.labels)
    expect(wrapper.vm.$props.graphData.datasets).toEqual(graphData.datasets)
  })

  it('renders different graph types', async () => {
    const wrapper = mount(GraphRenderer, {
      props: { graphData: { type: 'pie', labels: [], datasets: [] } },
      global: { stubs: { Pie: true } }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })
})
