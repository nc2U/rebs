import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import Company from '../Index.vue'

describe('Company app', () => {
  it('Company header title check', () => {
    const wrapper = shallowMount(Company, {
      global: {
        plugins: [createTestingPinia()],
      },
    })
    expect(wrapper.find('content-header-stub').attributes('pagetitle')).toBe('환경 설정')
    expect(wrapper.find('content-header-stub').attributes('navmenu')).toBe(
      '회사 정보 관리,권한 설정 관리,프로필 관리',
    )
  })
})
