import { describe, it, expect } from 'vitest'
import { mount, shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import AppHeaderDropdownAccnt from '@/layouts/containers/AppHeaderDropdownAccnt.vue'

const vuetify = createVuetify()

describe('AppHeaderDropdownAccnt Component Test', () => {
  it('should ', () => {
    const wrapper = mount(AppHeaderDropdownAccnt, {
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
