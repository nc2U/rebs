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
      global: {
        plugins: [createTestingPinia(), vuetify, CoreuiVue],
      },
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
    const wrapper = mount(CompanyForm, {
      global: {
        plugins: [vuetify, CoreuiVue],
        directives: {
          maska: vMaska,
        },
      },
      props: {
        company,
      },
    })

    console.log(wrapper.find('input#name').html())
    expect(wrapper.find('input#name').html())
    expect(wrapper.find('input#ceo').html())
    expect(wrapper.find('input#tax_number').html())
    expect(wrapper.find('input#org_number').html())
    expect(wrapper.find('input#business_cond').html())
    expect(wrapper.find('input#business_even').html())
    expect(wrapper.find('div#es_date').html())
    expect(wrapper.find('div#op_date').html())
    expect(wrapper.find('input#zipcode').html())
    expect(wrapper.find('input#address1').html())
    expect(wrapper.find('input#address2').html())
    expect(wrapper.find('input#address3').html())
  })
})
