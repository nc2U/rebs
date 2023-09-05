import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import MultiSelect from '../MultiSelect/index.vue'

describe('MultiSelect Component Test', () => {
  it('multiselect comp elements test', () => {
    const wrapper = mount(MultiSelect)

    expect(wrapper.find('.multiselect').exists()).toBeTruthy()

    expect(wrapper.find('.multiselect-wrapper').exists()).toBeTruthy()
    expect(wrapper.find('.multiselect-tags').exists()).toBeTruthy()
    expect(wrapper.find('.multiselect-tags-search-wrapper').exists()).toBeTruthy()
    expect(wrapper.find('span.multiselect-tags-search-copy').exists()).toBeTruthy()
    expect(wrapper.find('input.form-control.multiselect-tags-search').exists()).toBeTruthy()

    expect(wrapper.find('.multiselect-dropdown').exists()).toBeTruthy()
    expect(wrapper.find('ul.multiselect-options').exists()).toBeTruthy()
    expect(wrapper.find('div.multiselect-no-options').text()).toBe('The list is empty')
    expect(wrapper.find('.multiselect-spacer').exists()).toBeTruthy()
  })
})
