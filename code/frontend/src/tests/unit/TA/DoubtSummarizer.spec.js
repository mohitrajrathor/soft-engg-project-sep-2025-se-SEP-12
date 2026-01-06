import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import DoubtSummarizer from '@/components/TA/DoubtSummarizer.vue'
import doubtsAPI from '@/api/doubts'

// Mock the API module
vi.mock('@/api/doubts', () => ({
  default: {
    getSummary: vi.fn(() => Promise.resolve({
      topics: [{ topic: 'Test Topic', count: 5 }],
      topicClusters: [{ topic: 'Test Cluster', count: 10 }],
      learning_gaps: [{ gap: 'Test Gap', severity: 'high' }],
      stats: {
        total_messages: 50,
        topic_clusters: 5,
        recurring_issues: 3,
        learning_gaps_count: 2
      }
    })),
    getSourceBreakdown: vi.fn(() => Promise.resolve({
      total: 50,
      breakdown: { forum: 30, email: 15, chat: 5 }
    }))
  }
}))

describe('DoubtSummarizer.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the component without crashing', async () => {
    const wrapper = mount(DoubtSummarizer, {
      global: {
        stubs: {
          TASidebar: true,
          ExportOptions: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays the main title', async () => {
    const wrapper = mount(DoubtSummarizer, {
      global: {
        stubs: {
          TASidebar: true,
          ExportOptions: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Doubt Summarizer')
  })

  it('calls fetchSummary on mount', async () => {
    mount(DoubtSummarizer, {
      global: {
        stubs: {
          TASidebar: true,
          ExportOptions: true
        }
      }
    })
    await new Promise(resolve => setTimeout(resolve, 100))
    expect(doubtsAPI.getSummary).toHaveBeenCalled()
    expect(doubtsAPI.getSourceBreakdown).toHaveBeenCalled()
  })

  it('shows loading state initially', async () => {
    vi.spyOn(doubtsAPI, 'getSummary').mockImplementationOnce(() => new Promise(() => {}))
    const wrapper = mount(DoubtSummarizer, {
      global: {
        stubs: {
          TASidebar: true,
          ExportOptions: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.animate-pulse').exists()).toBe(true)
  })

  it('shows an error message if API call fails', async () => {
    const errorMessage = 'Failed to load summary'
    vi.spyOn(doubtsAPI, 'getSummary').mockRejectedValueOnce(new Error(errorMessage))
    const wrapper = mount(DoubtSummarizer, {
      global: {
        stubs: {
          TASidebar: true,
          ExportOptions: true
        }
      }
    })
    await new Promise(resolve => setTimeout(resolve, 200))
    expect(wrapper.text()).toContain('Error')
  })
})
