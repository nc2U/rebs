import { describe, it, expect } from 'vitest'

import { shallowMount } from '@vue/test-utils'
import BackToTop from '../BackToTop/index.vue'

describe('BackToTop', () => {
  it('BackToTop component', () => {
    const wrapper = shallowMount(BackToTop, {
      props: {
        customStyle: {
          right: '50px',
          bottom: '50px',
          width: '46px',
          height: '46px',
        },
        transitionName: 'fade',
      },
    })
    // console.log(wrapper.html())
    expect(wrapper.find('div').attributes('style')).toContain(
      'right: 50px; bottom: 50px; width: 46px; height: 46px;',
    )
    expect(wrapper.find('transition-stub').attributes('name')).toBe('fade')
  })
})
