import api from '@/api'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'

export interface Site {
  pk: number
  project: number
  order: number
  district: string
  lot_number: string
  site_purpose: string
  official_area: string
  returned_area: number | null
  rights_restrictions: string
  dup_issue_date: string
}

export interface SiteOwner {
  pk: number
  project: number
  owner: string
  date_of_birth: string | null
  phone1: string
  phone2: string
  zipcode: string
  address1: string
  address2: string
  address3: string
  own_sort: string
  own_sort_desc: string
  sites: number[]
  counsel_record: string
}

export interface SiteOwnshipRelationship {
  pk: number
  site: number
  site_owner: number
  ownership_ratio: number | null
  owned_area: number | null
  acquisition_date: string | null
}

export interface SiteContract {
  pk: number
  project: number
  owner: number
  contract_date: string
  total_price: number
  down_pay1: number
  down_pay1_is_paid: boolean
  down_pay2: number
  down_pay2_is_paid: boolean
  inter_pay1: number
  inter_pay1_date: string | null
  inter_pay1_is_paid: boolean
  inter_pay2: number
  inter_pay2_date: string | null
  inter_pay2_is_paid: boolean
  remain_pay: number
  remain_pay_date: string | null
  remain_pay_is_paid: boolean
  ownership_completion: boolean
  acc_bank: string
  acc_number: string
  acc_owner: string
  note: string
}

export const useSite = defineStore('site', () => {
  // states

  const siteList = ref<Site[]>([])
  const siteCount = ref(0)
  const siteOwnerList = ref<SiteOwner[]>([])
  const siteOwnerRelationList = ref<SiteOwnshipRelationship[]>([])
  const siteContractList = ref<SiteContract[]>([])

  const fetchSiteList = (project: string) => {
    api
      .get(`/site/?project=${project}`)
      .then(res => {
        siteList.value = res.data.results
        siteCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createSite = (payload: Site) => {
    api
      .post(`/site/`, payload)
      .then(res => {
        fetchSiteList(res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const updateSite = (payload: { pk: string } & Site) => {
    const { pk, ...siteData } = payload
    api
      .put(`/site/${pk}/`, siteData)
      .then(res => {
        fetchSiteList(res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteSite = (pk: string, project: string) => {
    api
      .delete(`/site/${pk}/`)
      .then(() => {
        fetchSiteList(project)
        message('warning', '', '삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  return {
    siteList,
    siteCount,
    siteOwnerList,
    siteOwnerRelationList,
    siteContractList,

    fetchSiteList,
    createSite,
    updateSite,
    deleteSite,
  }
})
