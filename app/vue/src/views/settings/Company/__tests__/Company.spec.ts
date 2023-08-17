import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import Company from '../Index.vue'
import CompanyDetail from '../components/CompanyDetail.vue'
import CompanyForm from '../components/CompanyForm.vue'

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

  it('Company Detail company date check...', () => {
    const wrapper = shallowMount(CompanyDetail, {
      props: {
        company,
      },
    })
    expect(wrapper.html()).toContain('코리아 주식회사')
    expect(wrapper.html()).toContain('홍길동')
    expect(wrapper.html()).toContain('주소1')
    expect(wrapper.html()).toContain('주소2')
    expect(wrapper.html()).toContain('주소3')
  })

  it('Company Form check', () => {
    const wrapper = shallowMount(CompanyForm, {
      props: {
        company,
      },
    })
    const inputs = wrapper.findAll('cforminput')
    expect(inputs[0].attributes('modelvalue')).toBe(company.name)
    expect(inputs[1].attributes('modelvalue')).toBe(company.ceo)
    expect(inputs[2].attributes('modelvalue')).toBe(company.business_cond)
    expect(inputs[3].attributes('modelvalue')).toBe(company.business_even)
    expect(inputs[4].attributes('modelvalue')).toBe(company.zipcode)
    expect(inputs[5].attributes('modelvalue')).toBe(company.address1)
    expect(inputs[6].attributes('modelvalue')).toBe(company.address2)
    expect(inputs[7].attributes('modelvalue')).toBe(company.address3)
  })
})
