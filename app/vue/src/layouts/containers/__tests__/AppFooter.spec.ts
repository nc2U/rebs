import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import CoreuiVue from '@coreui/vue'

import AppFooter from '@/layouts/containers/AppFooter.vue'

describe('AppFooter Component Test', () => {
  it('footer exists & 2 divs check', () => {
    const wrapper = mount(AppFooter, {
      global: {
        plugins: [CoreuiVue],
      },
    })

    expect(wrapper.find('.footer').exists()).toBeTruthy()
    expect(wrapper.find('.footer').findAll('div')).toHaveLength(2)
  })
})
