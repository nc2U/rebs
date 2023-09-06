import { describe, it, expect } from 'vitest'
import { shallowMount, mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createVuetify } from 'vuetify'
import { vMaska } from 'maska'
import CoreuiVue from '@coreui/vue'

import Company from '../Index.vue'
import CompanyDetail from '../components/CompanyDetail.vue'
import CompanyForm from '../components/CompanyForm.vue'

const vuetify = createVuetify()

describe('Company app test', () => {
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

  const company = {
    pk: 1,
    name: '코리아 주식회사',
    ceo: '홍길동',
    tax_number: '1234',
    org_number: '5678',
    business_cond: 'abc',
    business_even: 'def',
    es_date: '2020-01-01',
    op_date: '2020-01-02',
    zipcode: '12345',
    address1: '주소1',
    address2: '주소2',
    address3: '주소3',
  }

  it('Company Detail company date check...', async () => {
    const wrapper = mount(CompanyDetail, {
      props: {
        company,
      },
      global: {
        plugins: [createTestingPinia(), vuetify, CoreuiVue],
      },
    })
    
    expect(wrapper.html()).toContain('코리아 주식회사')
    expect(wrapper.html()).toContain('홍길동')
    expect(wrapper.html()).toContain('주소1')
    expect(wrapper.html()).toContain('주소2')
    expect(wrapper.html()).toContain('주소3')
  })

  it('Company Form check', async () => {
    const wrapper = mount(CompanyForm, {
      props: {
        company,
      },
      global: {
        plugins: [vuetify, CoreuiVue],
        directives: {
          maska: vMaska,
        },
      },
    })

    await wrapper.get('input[id=name]').setValue('korea inc.')
    await wrapper.get('input[id=ceo]').setValue('James')
    await wrapper.get('input[id=tax_number]').setValue('123-45-67890')
    await wrapper.get('input[id=org_number]').setValue('123456-2167890')
    await wrapper.get('input[id=business_cond]').setValue('a')
    await wrapper.get('input[id=business_even]').setValue('b')
    await wrapper.get('div[id=es_date]').find('input').setValue('2020-12-12')
    await wrapper.get('div[id=op_date]').find('input').setValue('2020-12-12')
    await wrapper.get('input[id=zipcode]').setValue('12345')
    await wrapper.get('input[id=address1]').setValue('abc')
    await wrapper.get('input[id=address2]').setValue('efg')
    await wrapper.get('input[id=address3]').setValue('xyz')

    await wrapper.find('form').trigger('submit.prevent')
  })
})
