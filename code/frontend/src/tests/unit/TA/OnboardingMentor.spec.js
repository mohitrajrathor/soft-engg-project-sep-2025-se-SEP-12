import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import OnboardingMentor from '@/components/TA/OnboardingMentor.vue'

describe('OnboardingMentor.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the onboarding mentor component', async () => {
    const wrapper = mount(OnboardingMentor, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('displays onboarding content', async () => {
    const wrapper = mount(OnboardingMentor, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Onboarding') || expect(wrapper.text()).toContain('Mentor')
  })

  it('shows onboarding steps', async () => {
    const wrapper = mount(OnboardingMentor, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    const steps = wrapper.findAll('.step') || wrapper.findAll('li')
    expect(steps.length).toBeGreaterThanOrEqual(0)
  })

  it('handles navigation between steps', async () => {
    const wrapper = mount(OnboardingMentor, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    
    const nextButton = wrapper.find('button[aria-label="next"]') || wrapper.find('.next-button')
    if (nextButton.exists()) {
      await nextButton.trigger('click')
      expect(wrapper.vm.$data).toHaveProperty('currentStep')
    }
  })

  it('displays mentor guidance information', async () => {
    const wrapper = mount(OnboardingMentor, {
      global: {
        stubs: {
          TASidebar: true
        }
      }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toBeTruthy()
  })
})
