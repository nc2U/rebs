import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import Company from '../Index.vue'

describe('Company app', () => {
  it('Company Index', () => {
    const wrapper = shallowMount(Company, {
      global: {
        plugins: [createTestingPinia()],
      },
    })
    expect(wrapper.find('content-header-stub').attributes('pagetitle')).toBe('환경 설정')
  })
})
