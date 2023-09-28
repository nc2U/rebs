import { describe, it, expect } from 'vitest'
import { mount, shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import CategoryTabs from '../Documents/CategoryTabs.vue'
import DocsForm from '../Documents/DocsForm.vue'
import DocsList from '../Documents/DocsList.vue'
import DocsView from '../Documents/DocsView.vue'
import ListController from '../Documents/ListController.vue'

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
