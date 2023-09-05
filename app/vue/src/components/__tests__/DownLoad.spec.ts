import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'

import PdfExport from '@/components/DownLoad/PdfExport.vue'
import ExcelExport from '@/components/DownLoad/ExcelExport.vue'

const vuetify = createVuetify()

describe('DownLoad Component Test', () => {
  it('pdf expoert test', async () => {
    const wrapper = mount(PdfExport, {
      global: {
        plugins: [vuetify],
        stubs: [],
      },
      props: {
        url: 'abc.com/content/1',
        disabled: false,
      },
    })

    expect(wrapper.html()).toContain('Pdf Export')
    expect(wrapper.find('a').attributes('href')).toBe('abc.com/content/1')
    expect(wrapper.find('a').attributes('disabled')).not.toBeTruthy()

    await wrapper.setProps({ disabled: true })

    expect(wrapper.find('a').attributes('disabled')).toBeTruthy()
  })

  it('excel expoert test', async () => {
    const wrapper = mount(ExcelExport, {
      global: {
        plugins: [vuetify],
      },
      props: {
        url: 'abc.com/content/2',
        disabled: false,
      },
    })

    expect(wrapper.html()).toContain('Excel Export')
    expect(wrapper.find('a').attributes('href')).toBe('abc.com/content/2')
    expect(wrapper.find('a').attributes('disabled')).not.toBeTruthy()

    await wrapper.setProps({ disabled: true })

    expect(wrapper.find('a').attributes('disabled')).toBeTruthy()
  })
})
