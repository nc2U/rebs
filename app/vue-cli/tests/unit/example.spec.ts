import { mount } from '@vue/test-utils'
import NotFound from '@/components/NotFound.vue'

describe('NotFound.vue', () => {
  it('renders NotFound component', () => {
    const msg = "But if you don't change your direction"
    const wrapper = mount(NotFound)
    expect(wrapper.text()).toMatch(msg)
  })
})
