import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccount } from '@/store/pinia/account'
import { errorHandle, message } from '@/utils/helper'

export interface Department {
  name: string
  task: string
}

interface Positions {
  pk: number
  rank: string
  title: string
  description: string
}

export interface Company {
  pk: number
  name: string
  ceo: string
  tax_number: string
  org_number: string
  business_cond: string
  business_even: string
  es_date: string
  op_date: string
  zipcode: string
  address1: string
  address2: string
  address3: string
  departments: Department[]
  positions: Positions[]
}

export const useCompany = defineStore('company', () => {
  // states
  const companyList = ref<Company[]>([])
  const company = ref<Company | null>(null)

  // getters
  const initComId = computed(() => {
    const account = useAccount()
    return account.userInfo?.staffauth?.company
      ? account.userInfo.staffauth.company
      : 1
  })

  const comSelect = computed(() => {
    return companyList.value.map((com: Company) => ({
      value: com.pk,
      text: com.name,
    }))
  })

  // actions
  const fetchCompanyList = () => {
    api
      .get('/company/')
      .then(res => (companyList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const fetchCompany = (pk: string) => {
    api
      .get(`/company/${pk}`)
      .then(res => (company.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }

  const createCompany = (payload: Company) => {
    api
      .post(`/company/`, payload)
      .then(res => {
        fetchCompany(res.data.pk)
        fetchCompanyList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const updateCompany = (payload: { pk: string } & Company) => {
    const { pk, ...comData } = payload
    api
      .put(`/company/${pk}/`, comData)
      .then(res => {
        fetchCompany(res.data.pk)
        fetchCompanyList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteCompany = (pk: string) => {
    api.delete(`/company/${pk}`).then(() => {
      fetchCompanyList()
      message('warning', '', '삭제되었습니다.')
    })
  }

  return {
    companyList,
    company,
    initComId,
    comSelect,
    fetchCompanyList,
    fetchCompany,
    createCompany,
    updateCompany,
    deleteCompany,
  }
})
