import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccount } from '@/store/pinia/account'
import { errorHandle, message } from '@/utils/helper'

export interface Project {
  pk: number
  company: number
  name: string
  order: number | null
  kind: string
  kind_desc: string
  start_year: string
  is_direct_manage: boolean
  is_returned_area: boolean
  is_unit_set: boolean
  local_zipcode: string | null
  local_address1: string | null
  local_address2: string | null
  local_address3: string | null
  area_usage: string | null
  build_size: string | null
  num_unit: number | null
  buy_land_extent: number | null
  scheme_land_extent: number | null
  donation_land_extent: number | null
  on_floor_area: number | null
  under_floor_area: number | null
  total_floor_area: number | null
  build_area: number | null
  floor_area_ratio: number | null
  build_to_land_ratio: number | null
  num_legal_parking: number | null
  num_planed_parking: number | null
}

export const useProject = defineStore('project', () => {
  // states
  const projectList = ref<Project[]>([])
  const project = ref<Project | null>(null)

  // getters
  const initProjId = computed(() => {
    const account = useAccount()
    return account.userInfo?.staffauth?.assigned_project
      ? account.userInfo.staffauth.assigned_project
      : account.userInfo?.staffauth?.allowed_projects[0] || 1
  })

  const allowed_projects = computed(() => {
    const account = useAccount()
    return account.userInfo && account.userInfo.staffauth
      ? account.userInfo.staffauth.allowed_projects
      : []
  })

  const projSelect = computed(() =>
    projectList.value
      ? projectList.value
          .filter((p: Project) => allowed_projects.value.includes(p.pk))
          .map((p: Project) => ({ value: p.pk, text: p.name }))
      : [],
  )

  // actions
  const fetchProjectList = () => {
    api
      .get('/project/')
      .then(res => (projectList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const fetchProject = (pk: string) => {
    api
      .get(`/project/${pk}/`)
      .then(res => (project.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }

  const createProject = (payload: Project) => {
    api
      .post('/project/', payload)
      .then(res => {
        fetchProject(res.data.pk)
        fetchProjectList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const updateProject = (payload: { pk: string } & Project) => {
    const { pk, ...projectData } = payload
    api
      .put(`/project/${pk}/`, projectData)
      .then(res => {
        fetchProject(res.data.pk)
        fetchProjectList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteProject = (pk: string) => {
    api
      .delete(`/project/${pk}/`)
      .then(() => {
        fetchProjectList()
        message('warning', '', '삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  return {
    projectList,
    project,
    initProjId,
    allowed_projects,
    projSelect,

    fetchProjectList,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
  }
})
