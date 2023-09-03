import { describe, expect, it } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import App from '@/App.vue'

const vuetify = createVuetify()

describe('App Component Test', () => {
  it('should ', () => {
    const wrapper = shallowMount(App, {
      global: {
        plugins: [createTestingPinia(), vuetify, CoreuiVue],
        stubs: ['router-view'],
      },
    })

    expect(wrapper.attributes('fullheight')).toBeTruthy()
  })
})
