import { describe, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import CategoryTabs from '../Documents/CategoryTabs.vue'

const vuetify = createVuetify()

describe('CategoryTabs Component Test', () => {
  it('should ', () => {
    const wrapper = mount(CategoryTabs, {
      global: {
        plugins: [createTestingPinia(), vuetify, CoreuiVue],
        mocks: {},
        provide: {},
        components: {},
        directives: {},
        stubs: [],
      },
      attrs: {},
      props: {},
      slots: {},
      shallow: true,
    })

    console.log(wrapper.html())
  })
})
