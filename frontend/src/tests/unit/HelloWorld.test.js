import { mount } from '@vue/test-utils'
import HelloWorld from '../../components/HelloWorld.vue'

describe('HelloWorld.vue', () => {
  it('renders the correct message', () => {
    const wrapper = mount(HelloWorld, {
      props: { msg: 'Hello, Vue!' },
    })
    expect(wrapper.text()).toContain('Hello, Vue!')
  })
})
