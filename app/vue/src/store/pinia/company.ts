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

interface Logo {
  pk: number
  company: number
  generic_logo: string
  dark_logo: string
  simple_logo: string
}

export const useCompany = defineStore('company', () => {
  // states
  const companyList = ref<Company[]>([])
  const company = ref<Company | null>(null)
  const logo = ref<Logo | null>(null)

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
      .get(`/company/${pk}/`)
      .then(res => (company.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }

  const fetchLogo = (pk: string) => {
    api
      .get(`/logo/${pk}/`)
      .then(res => (logo.value = res.data))
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

  const createLogo = (payload: Logo) => {
    api
      .post(`/logo/`, payload)
      .then(res => {
        fetchLogo(res.data.pk)
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

  const updateLogo = (payload: { pk: string } & Logo) => {
    const { pk, ...logoData } = payload
    api
      .put(`/logo/${pk}/`, logoData)
      .then(res => {
        fetchLogo(res.data.pk)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteCompany = (pk: string) => {
    api
      .delete(`/company/${pk}/`)
      .then(() => {
        fetchCompanyList()
        message('warning', '', '삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteLogo = (pk: string) => {
    api
      .delete(`/logo/${pk}/`)
      .then(() => message('warning', '', '삭제되었습니다.'))
      .catch(err => errorHandle(err.response.data))
  }

  return {
    companyList,
    company,
    logo,
    initComId,
    comSelect,

    fetchCompanyList,
    fetchCompany,
    fetchLogo,
    createCompany,
    createLogo,
    updateCompany,
    updateLogo,
    deleteCompany,
    deleteLogo,
  }
})
