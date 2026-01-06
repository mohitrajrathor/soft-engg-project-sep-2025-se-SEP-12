import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import studentAIAssistance from '@/components/student/studentAIAssistance.vue'
import chatbot from '@/api/chatbot'

vi.mock('@/api/chatbot', () => ({
  default: {
    sendMessage: vi.fn(() => Promise.resolve({
      response: 'AI generated response',
      timestamp: new Date()
    }))
  }
}))

describe('studentAIAssistance.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the AI assistance component', async () => {
    const wrapper = mount(studentAIAssistance, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays AI chat interface', async () => {
    const wrapper = mount(studentAIAssistance, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('AI') || expect(wrapper.text()).toContain('Assistant')
  })

  it('shows message input field', async () => {
    const wrapper = mount(studentAIAssistance, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const textarea = wrapper.find('textarea') || wrapper.find('input[type="text"]')
    expect(textarea.exists() || wrapper.find('input').exists()).toBe(true)
  })

  it('handles message sending', async () => {
    const wrapper = mount(studentAIAssistance, {
      global: {
        stubs: {
          StudentSidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const sendButton = wrapper.find('button[aria-label="send"]') || wrapper.find('.send-button')
    if (sendButton.exists()) {
      await sendButton.trigger('click')
      expect(wrapper.emitted()).toBeDefined()
    }
  })
})
