import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import Spinner from '../Spinner/index.vue'

describe('Spinner Component Test', () => {
  it('spinner comp test', async () => {
    const wrapper = mount(Spinner, {
      props: {
        loading: true,
      },
    })

    expect(wrapper.find('.modal').exists()).toBeTruthy()
    expect(wrapper.find('.lds-facebook').exists()).toBeTruthy()
    expect(wrapper.find('.lds-facebook').findAll('div')).toHaveLength(3)

    await wrapper.setProps({ loading: false })

    expect(wrapper.find('.modal').exists()).toBeFalsy()
  })
})
