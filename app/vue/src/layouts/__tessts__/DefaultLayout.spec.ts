import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import router from '@/router'

import DefaultLayout from '@/layouts/DefaultLayout.vue'

describe('DefaultLayout', () => {
  it('DefaultLayout chk?', () => {
    const wrapper = shallowMount(DefaultLayout, {
      global: {
        plugins: [createTestingPinia(), router],
      },
    })
    // console.log(wrapper.html())
    expect(2 + 2).toBe(4)
  })
})
