import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import AppSidebar from '@/layouts/containers/AppSidebar.vue'

const vuetify = createVuetify()

describe('AppSidebar Component Test', () => {
  it('sidebar brand, nav & toggler check', () => {
    const wrapper = mount(AppSidebar, {
      global: {
        plugins: [createTestingPinia(), vuetify, CoreuiVue],
        stubs: ['CIcon', 'app-sidebar-nav'],
      },
    })

    const brand = wrapper.find('.sidebar-brand')

    expect(brand.html()).toContain('sidebar-brand-full')
    expect(brand.html()).toContain('sidebar-brand-narrow')
    expect(wrapper.html()).toContain('app-sidebar-nav')
    expect(wrapper.find('button').classes()).toContain('sidebar-toggler')
  })
})
