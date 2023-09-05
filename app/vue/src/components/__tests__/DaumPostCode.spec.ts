import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import DaumPostCode from '@/components/DaumPostcode/index.vue'

describe('DaumPostCode Component Test', () => {
  it('Daum post code layer test', () => {
    const wrapper = mount(DaumPostCode, {
      global: {
        plugins: [createTestingPinia()],
      },
    })

    expect(wrapper.find('#layer').exists()).toBeTruthy()
    expect(wrapper.find('img[id=btnCloseLayer]').exists()).toBeTruthy()
  })
})
