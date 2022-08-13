import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { Company } from '@/store/modules/settings/state'
import { errorHandle, message } from '@/utils/helper'

export const useCompany = defineStore('company', () => {
  // states
  const companyList = ref<Company[]>([])
  const company = ref<Company | null>(null)

  // getters
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
    comSelect,
    fetchCompanyList,
    fetchCompany,
    createCompany,
    updateCompany,
    deleteCompany,
  }
})
