import { describe, expect, it } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import AppAside from '@/layouts/containers/AppAside.vue'

const vuetify = createVuetify()

describe('AppAside Component Test', () => {
  it('sidebar exsists check', () => {
    const wrapper = shallowMount(AppAside, {
      global: {
        plugins: [createTestingPinia(), vuetify, CoreuiVue],
        stubs: ['CIcon'],
      },
      props: {
        position: 'fixed',
      },
    })

    expect(wrapper.html()).toContain('c-sidebar-stub')
  })
})
