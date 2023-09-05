import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import Pagination from '../Pagination'

describe('Pagination Component Test', () => {
  it('pagination comp test', async () => {
    const wrapper = mount(Pagination, {
      props: {
        align: 'start',
        activePage: 1,
        limit: 5,
      },
    })

    expect(wrapper.find('nav.justify-content-start').exists()).toBeTruthy()
    expect(wrapper.find('ul.pagination').exists()).toBeTruthy()
    expect(wrapper.find('li.page-item[aria-label="Go to first page"]').exists()).toBeTruthy()
    expect(wrapper.find('li.page-item[aria-label="Go to previous page"]').exists()).toBeTruthy()

    expect(wrapper.find('li.page-item.active').text()).toBe('1')

    expect(wrapper.find('li.page-item[aria-label="Go to next page"]').exists()).toBeTruthy()
    expect(wrapper.find('li.page-item[aria-label="Go to last page"]').exists()).toBeTruthy()

    await wrapper.setProps({ align: 'end' })
    await wrapper.setProps({ activePage: 3 })

    expect(wrapper.find('nav.justify-content-end').exists()).toBeTruthy()
    expect(wrapper.find('li.page-item.active').text()).toBe('3')
  })
})
