import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import BlankComponent from '../BlankComponent.vue'

const vuetify = createVuetify()

describe('BlankComponent Component Test', () => {
  it('Blank comp test', () => {
    const wrapper = mount(BlankComponent, {
      global: {
        plugins: [vuetify, CoreuiVue],
        stubs: ['CIcon'],
      },
    })

    expect(wrapper.find('.card').exists()).toBeTruthy()
    expect(wrapper.find('.card').findAll('div')).toHaveLength(3)
    expect(wrapper.find('.card-header').exists()).toBeTruthy()
    expect(wrapper.find('.card-header').text()).toBe('Subpage Title')
    expect(wrapper.find('.card-body').exists()).toBeTruthy()
    expect(wrapper.find('.card-footer').exists()).toBeTruthy()
  })
})
