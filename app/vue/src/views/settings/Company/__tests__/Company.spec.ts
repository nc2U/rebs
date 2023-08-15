import { describe, it, expect } from 'vitest'
import { shallowMount, mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import Company from '../Index.vue'

describe('Company app', () => {
  it('Company Index', () => {
    const wrapper = mount(Company, {
      global: {
        plugins: [createTestingPinia()],
      },
    })
    console.log(wrapper.html())
  })
})
