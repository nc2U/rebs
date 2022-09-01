import api from '@/api'
import { ref, computed } from 'vue'
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
  returned_area: string | null
  rights_restrictions: string
  dup_issue_date: string
  owners: { pk: number; owner: string }[]
}

export interface SiteOwner {
  pk: number | null
  project: number | null
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
  sites: {
    pk: number
    site: number
    __str__: string
    ownership_ratio: string
    owned_area: string
    acquisition_date: string | null
  }[]
  counsel_record: string
}

export interface Relation {
  pk: number | null
  site: number | null
  site_owner: number | null
  ownership_ratio: string
  owned_area: string
  acquisition_date: null | string
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

interface AllSite {
  pk: number
  __str__: string
}

export const useSite = defineStore('site', () => {
  // states

  const allSites = ref<AllSite[]>([])
  const getSites = computed(() =>
    allSites.value.map((s: AllSite) => ({
      value: s.pk,
      label: s.__str__,
    })),
  )

  const fetchAllSites = (project: number) => {
    api.get(`/all-site/?project=${project}`).then(res => {
      allSites.value = res.data.results
    })
  }

  const siteList = ref<Site[]>([])
  const getSiteList = computed(() =>
    siteList.value.map((s: Site) => ({
      pk: s.pk,
      project: s.project,
      order: s.order,
      district: s.district,
      lot_number: s.lot_number,
      site_purpose: s.site_purpose,
      official_area: s.official_area,
      returned_area: s.returned_area,
      rights_restrictions: s.rights_restrictions,
      dup_issue_date: s.dup_issue_date,
      owners: s.owners.map(o => o.owner),
    })),
  )
  const siteCount = ref(0)

  const fetchSiteList = (project: number, page = 1, search = '') => {
    api
      .get(`/site/?project=${project}&page=${page}&search=${search}`)
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

  const updateSite = (payload: { pk: number } & Site) => {
    const { pk, ...siteData } = payload
    api
      .put(`/site/${pk}/`, siteData)
      .then(res => {
        fetchSiteList(res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteSite = (pk: number, project: number) => {
    api
      .delete(`/site/${pk}/`)
      .then(() => {
        fetchSiteList(project)
        message('warning', '', '해당 부지 정보가 삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  const siteOwnerList = ref<SiteOwner[]>([])
  const siteOwnerCount = ref(0)

  const fetchSiteOwnerList = (
    project: number,
    page = 1,
    own_sort = '',
    search = '',
  ) => {
    api
      .get(
        `/site-owner/?project=${project}&page=${page}&own_sort=${own_sort}&search=${search}`,
      )
      .then(res => {
        siteOwnerList.value = res.data.results
        siteOwnerCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createSiteOwner = (payload: SiteOwner) => {
    api
      .post(`/site-owner/`, payload)
      .then(res => {
        // res.data.sites
        //   .forEach((site: number) => {
        //     api.post('/site-relation/', { site, site_owner: res.data.pk })
        //   })
        //   .finally(() => console.log('------------------>>>'))
        fetchSiteOwnerList(res.data.project)
        message()
        console.log('--->', res.data, res.data.sites)
      })
      .catch(err => errorHandle(err.response.data))
  }

  const updateSiteOwner = (payload: SiteOwner) => {
    const { pk, ...siteData } = payload
    api
      .put(`/site-owner/${pk}/`, siteData)
      .then(res => {
        fetchSiteOwnerList(res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteSiteOwner = (pk: number, project: number) => {
    api
      .delete(`/site-owner/${pk}/`)
      .then(() => {
        fetchSiteOwnerList(project)
        message('warning', '', '해당 소유자 정보가 삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  const relationList = ref<Relation[]>([])

  const patchRelation = (payload: Relation & { project: number }) => {
    const { pk, project, ...relationData } = payload
    api
      .patch(`/site-relation/${pk}/`, relationData)
      .then(() => {
        fetchSiteOwnerList(project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const siteContList = ref<SiteContract[]>([])
  const siteContCount = ref(0)

  const fetchSiteContList = (project: number, page = 1, search = '') => {
    api
      .get(`/site-contract/?project=${project}&page=${page}&search=${search}`)
      .then(res => {
        siteContList.value = res.data.results
        siteContCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createSiteCont = (payload: SiteContract) => {
    api
      .post(`/site-contract/`, payload)
      .then(res => {
        fetchSiteContList(res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const updateSiteCont = (payload: { pk: number } & SiteContract) => {
    const { pk, ...contData } = payload
    api
      .put(`/site-contract/${pk}/`, contData)
      .then(res => {
        fetchSiteContList(res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteSiteCont = (pk: number, project: number) => {
    api
      .delete(`/site-contract/${pk}/`)
      .then(() => {
        fetchSiteContList(project)
        message('warning', '', '해당 부지 매입계약 정보가 삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  return {
    allSites,
    getSites,
    fetchAllSites,

    siteList,
    getSiteList,
    siteCount,

    fetchSiteList,
    createSite,
    updateSite,
    deleteSite,

    siteOwnerList,
    siteOwnerCount,

    fetchSiteOwnerList,
    createSiteOwner,
    updateSiteOwner,
    deleteSiteOwner,

    relationList,

    patchRelation,

    siteContList,
    siteContCount,

    fetchSiteContList,
    createSiteCont,
    updateSiteCont,
    deleteSiteCont,
  }
})
