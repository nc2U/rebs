import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import BlankComponent from '@/components/BlankComponent.vue'

describe('BlankComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(BlankComponent)
    expect(wrapper.text()).toContain('Subpage Title')
  })
})
