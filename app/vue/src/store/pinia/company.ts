import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccount } from '@/store/pinia/account'
import { errorHandle, message } from '@/utils/helper'
import { Company, Logo } from '@/store/types/settings'
import {
  Staff,
  StaffFilter,
  Grade,
  Department,
  DepFilter,
  ComFilter,
} from '@/store/types/company'

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

  const staffList = ref<Grade[]>([])
  const staff = ref<Grade | null>(null)
  const staffsCount = ref<number>(0)

  // actions
  const staffPages = (itemsPerPage: number) =>
    Math.ceil(staffsCount.value / itemsPerPage)

  const fetchStaffList = (payload: StaffFilter) => {
    const {
      page = 1,
      com = 1,
      sort = '',
      dep = '',
      gra = '',
      pos = '',
      dut = '',
      sts = '',
      q = '',
    } = payload
    const qStr = `?page=${page}&company=${com}&sort=${sort}&department=${dep}&grade=${gra}&position=${pos}&duty=${dut}&status=${sts}&search=${q}`

    return api
      .get(`/staff/${qStr}`)
      .then(res => {
        staffList.value = res.data.results
        staffsCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const fetchStaff = (pk: number) =>
    api
      .get(`/staff/${pk}/`)
      .then(res => (staff.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createStaff = (payload: Staff, page = 1, com = 1) =>
    api
      .post(`/staff/`, payload)
      .then(res =>
        fetchStaffList({ page, com }).then(() =>
          fetchStaff(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateStaff = (payload: Staff, page = 1, com = 1) =>
    api
      .put(`/staff/${payload.pk}/`, payload)
      .then(res => {
        fetchStaffList({ page, com }).then(() =>
          fetchStaff(res.data.pk).then(() => message()),
        )
      })
      .catch(err => errorHandle(err.response.data))

  const deleteStaff = (pk: number, com = 1) =>
    api
      .delete(`/staff/${pk}/`)
      .then(() =>
        fetchStaffList({ com }).then(() =>
          message('warning', '', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const departmentList = ref<Department[]>([])
  const allDepartList = ref<Department[]>([])
  const department = ref<Department | null>(null)

  const departmentsCount = ref<number>(0)

  // getters
  const getPkDeparts = computed(() =>
    allDepartList.value.map(d => ({
      value: d.pk,
      label: d.name,
      level: d.level,
    })),
  )

  const getSlugDeparts = computed(() =>
    allDepartList.value.map(d => ({
      value: d.name,
      label: d.name,
    })),
  )

  const getUpperDeps = computed(() => [
    ...new Set(
      allDepartList.value
        .filter(d => !!d.upper_depart)
        .map(d => d.upper_depart),
    ),
  ])

  // actions
  const departmentPages = (itemsPerPage: number) =>
    Math.ceil(departmentsCount.value / itemsPerPage)

  const fetchDepartmentList = (payload: DepFilter) => {
    const { page = 1, com = 1, upp = '', q = '' } = payload
    const queryStr = `?page=${page}&company=${com}&upper_depart=${upp}&search=${q}`

    return api
      .get(`/department/${queryStr}`)
      .then(res => {
        departmentList.value = res.data.results
        departmentsCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const fetchAllDepartList = (com = 1) =>
    api
      .get(`/all-departs/?company=${com}`)
      .then(res => {
        allDepartList.value = res.data.results
      })
      .catch(err => errorHandle(err.response.data))

  const fetchDepartment = (pk: number) =>
    api
      .get(`/department/${pk}/`)
      .then(res => (department.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createDepartment = (payload: Department, page = 1, com = 1) =>
    api
      .post(`/department/`, payload)
      .then(res =>
        fetchDepartmentList({ page, com }).then(() =>
          fetchDepartment(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateDepartment = (payload: Department, page = 1, com = 1) =>
    api
      .put(`/department/${payload.pk}/`, payload)
      .then(res =>
        fetchDepartmentList({ page, com }).then(() =>
          fetchDepartment(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteDepartment = (pk: number, com = 1) =>
    api
      .delete(`/department/${pk}/`)
      .then(() =>
        fetchDepartmentList({ com }).then(() =>
          message('warning', '', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const gradeList = ref<Grade[]>([])
  const allGradeList = ref<Grade[]>([])
  const grade = ref<Grade | null>(null)
  const gradesCount = ref<number>(0)

  // getters
  const getGrades = computed(() =>
    allGradeList.value.map(r => ({
      value: r.grade,
      label: r.grade,
    })),
  )

  const getPkGrades = computed(() =>
    allGradeList.value.map(r => ({
      value: r.pk,
      label: r.grade,
    })),
  )

  // actions
  const gradePages = (itemsPerPage: number) =>
    Math.ceil(gradesCount.value / itemsPerPage)

  const fetchGradeList = (payload: ComFilter) => {
    const { page = 1, com = 1, q = '' } = payload
    const queryStr = `?page=${page}&company=${com}&search=${q}`
    return api
      .get(`/grade/${queryStr}`)
      .then(res => {
        gradeList.value = res.data.results
        gradesCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const fetchAllGradeList = (com = 1) =>
    api
      .get(`/all-grades/?company=${com}`)
      .then(res => {
        allGradeList.value = res.data.results
      })
      .catch(err => errorHandle(err.response.data))

  const fetchGrade = (pk: number) =>
    api
      .get(`/grade/${pk}/`)
      .then(res => (grade.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createGrade = (payload: Grade, page = 1, com = 1) =>
    api
      .post(`/grade/`, payload)
      .then(res =>
        fetchGradeList({ page, com }).then(() =>
          fetchGrade(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateGrade = (payload: Grade, page = 1, com = 1) =>
    api
      .put(`/grade/${payload.pk}/`, payload)
      .then(res => {
        fetchGradeList({ page, com }).then(() =>
          fetchGrade(res.data.pk).then(() => message()),
        )
      })
      .catch(err => errorHandle(err.response.data))

  const deleteGrade = (pk: number, com = 1) =>
    api
      .delete(`/grade/${pk}/`)
      .then(() =>
        fetchGradeList({ com }).then(() =>
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

    staffList,
    staff,
    staffsCount,
    staffPages,
    fetchStaffList,
    fetchStaff,
    createStaff,
    updateStaff,
    deleteStaff,

    departmentList,
    department,
    departmentsCount,
    getPkDeparts,
    getSlugDeparts,
    getUpperDeps,
    departmentPages,
    fetchDepartmentList,
    fetchAllDepartList,
    fetchDepartment,
    createDepartment,
    updateDepartment,
    deleteDepartment,

    gradeList,
    grade,
    gradesCount,
    getGrades,
    getPkGrades,
    gradePages,
    fetchGradeList,
    fetchAllGradeList,
    fetchGrade,
    createGrade,
    updateGrade,
    deleteGrade,
  }
})
