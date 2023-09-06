import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import CoreuiVue from '@coreui/vue'

import NotFound from '../NotFound.vue'

const vuetify = createVuetify()

describe('NotFound Component Test', () => {
  it('Notfound comp test', async () => {
    const wrapper = mount(NotFound, {
      global: {
        plugins: [vuetify, CoreuiVue],
        mocks: {
          $route: {
            name: 'some-title',
            meta: {
              title: null as string | null,
            },
          },
        },
      },
    })

    expect(wrapper.find('.card-header').exists()).toBeTruthy()
    expect(wrapper.find('.card-body').exists()).toBeTruthy()
    expect(wrapper.find('p').text()).toBe('404')
    expect(wrapper.find('h1.title').text()).toBe('PAGE NOT FOUND')
    expect(wrapper.find('blockquote.quote').text()).toContain("But if you don't")
    expect(wrapper.findAll('button')[0].text()).toBe('To previous')
    expect(wrapper.findAll('button')[1].text()).toBe('Take me home')
    expect(wrapper.find('.card-footer').exists()).toBeTruthy()
  })
})
