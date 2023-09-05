import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import AlertModal from '../Modals/AlertModal.vue'
import ConfirmModal from '../Modals/ConfirmModal.vue'
import FormModal from '../Modals/FormModal.vue'
import TodoModal from '../Modals/TodoModal.vue'

const vuetify = createVuetify()

describe('Modal Component Test', () => {
  it('AlertModal unit test', () => {
    const wrapper = mount(AlertModal, {
      global: {
        plugins: [vuetify, CoreuiVue],
      },
    })

    expect(wrapper.find('transition-stub[css=false]').exists()).toBeTruthy()
    expect(wrapper.find('transition-stub[css=true]').exists()).toBeTruthy()
  })

  it('ConfirmModal unit test', () => {
    const wrapper = mount(ConfirmModal, {
      global: {
        plugins: [vuetify, CoreuiVue],
      },
    })

    expect(wrapper.find('transition-stub[css=false]').exists()).toBeTruthy()
    expect(wrapper.find('transition-stub[css=true]').exists()).toBeTruthy()
  })

  it('FormModal unit test', () => {
    const wrapper = mount(FormModal, {
      global: {
        plugins: [vuetify, CoreuiVue],
      },
    })

    expect(wrapper.find('transition-stub[css=false]').exists()).toBeTruthy()
    expect(wrapper.find('transition-stub[css=true]').exists()).toBeTruthy()
  })

  it('TodoModal unit test', () => {
    const wrapper = mount(TodoModal, {
      global: {
        plugins: [vuetify, CoreuiVue],
        stubs: ['CIcon'],
      },
    })

    expect(wrapper.find('transition-stub[css=false]').exists()).toBeTruthy()
    expect(wrapper.find('transition-stub[css=true]').exists()).toBeTruthy()
  })
})
