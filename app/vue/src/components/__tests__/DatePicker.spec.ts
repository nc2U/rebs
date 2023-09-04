import { describe, it, expect } from 'vitest'
import { mount, shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import DatePicker from '../DatePicker/index.vue'

const vuetify = createVuetify()

describe('DatePicker Component Test', () => {
  it('should ', () => {
    const wrapper = mount(DatePicker, {
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
    })

    console.log(wrapper.html())
    // console.log(wrapper.find('input').html())
  })
})
