import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccount } from '@/store/pinia/account'
import { errorHandle, message } from '@/utils/helper'
import { Company, Logo } from '@/store/types/settings'

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

  const fetchCompany = (pk: number) => {
    api
      .get(`/company/${pk}/`)
      .then(res => (company.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }

  const fetchLogo = (pk: number) => {
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

  const updateCompany = (payload: { pk: number } & Company) => {
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

  const updateLogo = (payload: { pk: number } & Logo) => {
    const { pk, ...logoData } = payload
    api
      .put(`/logo/${pk}/`, logoData)
      .then(res => {
        fetchLogo(res.data.pk)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteCompany = (pk: number) => {
    api
      .delete(`/company/${pk}/`)
      .then(() => {
        fetchCompanyList()
        message('warning', '', '삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteLogo = (pk: number) => {
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
