import { describe, expect, it } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import TodoListApp from '../TodoListApp/index.vue'

describe('TodoListApp Component Test', () => {
  it('Todo list test', () => {
    const wrapper = shallowMount(TodoListApp, {
      global: {
        plugins: [createTestingPinia()],
      },
    })

    // header check
    expect(wrapper.find('header.header').exists()).toBeTruthy()
    expect(wrapper.find('header').find('input.new-todo').exists()).toBeTruthy()

    // section
    expect(wrapper.find('section.main').exists()).toBeTruthy()
    expect(wrapper.find('section').find('ul.todo-list').exists()).toBeTruthy()

    // footer
    expect(wrapper.find('footer.footer').exists()).toBeTruthy()
    expect(wrapper.find('footer.footer').find('ul.filters').exists()).toBeTruthy()
    expect(wrapper.find('ul.filters').findAll('li')).toHaveLength(3)
    expect(wrapper.find('button.clear-completed').exists()).toBeTruthy()
    expect(wrapper.find('footer.info').text()).toBe('첫 번째 할 일 목록을 메모해 보세요.')
  })
})
