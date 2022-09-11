import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccount } from '@/store/pinia/account'
import { errorHandle, message } from '@/utils/helper'
import { Company, Logo } from '@/store/types/settings'

const accountStore = useAccount()

export const useCompany = defineStore('company', () => {
  // states & getters
  const companyList = ref<Company[]>([])
  const company = ref<Company | null>(null)

  const initComId = computed(() =>
    accountStore.userInfo?.staffauth?.company
      ? accountStore.userInfo.staffauth.company
      : 1,
  )

  const comSelect = computed(() => {
    return companyList.value.map((com: Company) => ({
      value: com.pk,
      text: com.name,
    }))
  })

  // actions
  const fetchCompanyList = () =>
    api
      .get('/company/')
      .then(res => (companyList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchCompany = (pk: number) =>
    api
      .get(`/company/${pk}/`)
      .then(res => (company.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createCompany = (payload: Company) =>
    api
      .post(`/company/`, payload)
      .then(res =>
        fetchCompanyList().then(() =>
          fetchCompany(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateCompany = (payload: Company) =>
    api
      .put(`/company/${payload.pk}/`, payload)
      .then(res => fetchCompany(res.data.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteCompany = (pk: number) =>
    api
      .delete(`/company/${pk}/`)
      .then(() =>
        fetchCompanyList().then(() =>
          message('warning', '', '삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // states & getters
  const logo = ref<Logo | null>(null)

  const fetchLogo = (pk: number) =>
    api
      .get(`/logo/${pk}/`)
      .then(res => (logo.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createLogo = (payload: Logo) =>
    api
      .post(`/logo/`, payload)
      .then(res => fetchLogo(res.data.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const updateLogo = (payload: Logo) =>
    api
      .put(`/logo/${payload.pk}/`, payload)
      .then(res => fetchLogo(res.data.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteLogo = (pk: number) =>
    api
      .delete(`/logo/${pk}/`)
      .then(() => message('warning', '', '삭제되었습니다.'))
      .catch(err => errorHandle(err.response.data))

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

    logo,
    fetchLogo,
    createLogo,
    updateLogo,
    deleteLogo,
  }
})
