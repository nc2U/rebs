import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccount } from '@/store/pinia/account'
import { errorHandle, message } from '@/utils/helper'
import { Company, Logo } from '@/store/types/settings'
import { Department, Rank, Staff } from '@/store/types/company'

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
      label: com.name,
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
          message('warning', '', '해당 오브젝트가 삭제되었습니다.'),
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
      .then(() => message('warning', '', '해당 오브젝트가 삭제되었습니다.'))
      .catch(err => errorHandle(err.response.data))

  const departmentList = ref<Department[]>([])
  const allDepartList = ref<Department[]>([])
  const department = ref<Department | null>(null)

  const departmentsCount = ref<number>(0)

  // getters
  const getDeparts = computed(() =>
    allDepartList.value.map(d => ({
      value: d.pk,
      label: d.name,
      level: d.level,
    })),
  )

  // actions
  const departmentPages = (itemsPerPage: number) =>
    Math.ceil(departmentsCount.value / itemsPerPage)

  const fetchDepartmentList = (page = 1) =>
    api
      .get(`/department/?page=${page}`)
      .then(res => {
        departmentList.value = res.data.results
        departmentsCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))

  const fetchAllDepartList = () =>
    api
      .get(`/all-departs/`)
      .then(res => {
        allDepartList.value = res.data.results
      })
      .catch(err => errorHandle(err.response.data))

  const fetchDepartment = (pk: number) =>
    api
      .get(`/department/${pk}/`)
      .then(res => (department.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createDepartment = (payload: Department, page = 1) =>
    api
      .post(`/department/`, payload)
      .then(res =>
        fetchDepartmentList(page).then(() =>
          fetchDepartment(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateDepartment = (payload: Department, page = 1) =>
    api
      .put(`/department/${payload.pk}/`, payload)
      .then(res =>
        fetchDepartmentList(page).then(() =>
          fetchDepartment(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteDepartment = (pk: number) =>
    api
      .delete(`/department/${pk}/`)
      .then(() =>
        fetchDepartmentList().then(() =>
          message('warning', '', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const rankList = ref<Rank[]>([])
  const allRankList = ref<Rank[]>([])
  const rank = ref<Rank | null>(null)
  const ranksCount = ref<number>(0)

  // getters
  const getRanks = computed(() =>
    allRankList.value.map(r => ({
      value: r.pk,
      label: r.rank,
    })),
  )

  // actions
  const rankPages = (itemsPerPage: number) =>
    Math.ceil(ranksCount.value / itemsPerPage)

  const fetchRankList = (page = 1) =>
    api
      .get(`/rank/?page=${page}`)
      .then(res => {
        rankList.value = res.data.results
        ranksCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))

  const fetchAllRankList = () =>
    api
      .get(`/all-ranks/`)
      .then(res => {
        allRankList.value = res.data.results
      })
      .catch(err => errorHandle(err.response.data))

  const fetchRank = (pk: number) =>
    api
      .get(`/rank/${pk}/`)
      .then(res => (rank.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createRank = (payload: Rank, page = 1) =>
    api
      .post(`/rank/`, payload)
      .then(res =>
        fetchRankList(page).then(() =>
          fetchRank(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateRank = (payload: Rank, page = 1) =>
    api
      .put(`/rank/${payload.pk}/`, payload)
      .then(res => {
        fetchRankList(page).then(() =>
          fetchRank(res.data.pk).then(() => message()),
        )
      })
      .catch(err => errorHandle(err.response.data))

  const deleteRank = (pk: number) =>
    api
      .delete(`/rank/${pk}/`)
      .then(() =>
        fetchRankList().then(() =>
          message('warning', '', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const staffList = ref<Rank[]>([])
  const staff = ref<Rank | null>(null)
  const staffsCount = ref<number>(0)

  // actions
  const staffPages = (itemsPerPage: number) =>
    Math.ceil(staffsCount.value / itemsPerPage)

  const fetchStaffList = (page = 1) =>
    api
      .get(`/staff/?page=${page}`)
      .then(res => {
        staffList.value = res.data.results
        staffsCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))

  const fetchStaff = (pk: number) =>
    api
      .get(`/staff/${pk}/`)
      .then(res => (staff.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createStaff = (payload: Staff, page = 1) =>
    api
      .post(`/staff/`, payload)
      .then(res =>
        fetchStaffList(page).then(() =>
          fetchStaff(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateStaff = (payload: Staff, page = 1) =>
    api
      .put(`/staff/${payload.pk}/`, payload)
      .then(res => {
        fetchStaffList(page).then(() =>
          fetchStaff(res.data.pk).then(() => message()),
        )
      })
      .catch(err => errorHandle(err.response.data))

  const deleteStaff = (pk: number) =>
    api
      .delete(`/staff/${pk}/`)
      .then(() =>
        fetchStaffList().then(() =>
          message('warning', '', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
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

    departmentList,
    department,
    departmentsCount,
    getDeparts,
    departmentPages,
    fetchDepartmentList,
    fetchAllDepartList,
    fetchDepartment,
    createDepartment,
    updateDepartment,
    deleteDepartment,

    rankList,
    rank,
    ranksCount,
    getRanks,
    rankPages,
    fetchRankList,
    fetchAllRankList,
    fetchRank,
    createRank,
    updateRank,
    deleteRank,

    staffList,
    staff,
    staffsCount,
    staffPages,
    fetchStaffList,
    fetchStaff,
    createStaff,
    updateStaff,
    deleteStaff,
  }
})
