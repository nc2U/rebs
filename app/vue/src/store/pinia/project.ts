import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccount } from '@/store/pinia/account'
import { errorHandle, message } from '@/utils/helper'
import { Project, ProjectBudget } from '@/store/types/project'

const accountStore = useAccount()

export const useProject = defineStore('project', () => {
  // states & getters
  const projectList = ref<Project[]>([])
  const project = ref<Project | null>(null)

  const initProjId = computed(() =>
    accountStore.userInfo?.staffauth?.assigned_project
      ? accountStore.userInfo.staffauth.assigned_project
      : 1,
  )

  const allowed_projects = computed(() =>
    accountStore.userInfo && accountStore.userInfo.staffauth
      ? accountStore.userInfo.staffauth.allowed_projects
      : [],
  )

  const projSelect = computed(() => {
    const allowedProject = accountStore.superAuth
      ? projectList.value
      : projectList.value.filter((p: Project) =>
          allowed_projects.value.includes(p.pk || 0),
        )

    return allowedProject.map((p: Project) => ({ value: p.pk, text: p.name }))
  })

  const projectBudgetList = ref<ProjectBudget[]>([])

  // actions
  const fetchProjectList = () =>
    api
      .get('/project/')
      .then(res => (projectList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchProject = (pk: number) =>
    api
      .get(`/project/${pk}/`)
      .then(res => (project.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createProject = (payload: Project) => {
    api
      .post('/project/', payload)
      .then(res =>
        fetchProjectList().then(() =>
          fetchProject(res.data.pk).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))
  }

  const updateProject = (payload: Project) =>
    api
      .put(`/project/${payload.pk}/`, payload)
      .then(res => fetchProject(res.data.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteProject = (pk: number) =>
    api
      .delete(`/project/${pk}/`)
      .then(() =>
        fetchProjectList().then(() =>
          message('warning', '', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  return {
    projectList,
    project,
    initProjId,
    allowed_projects,
    projSelect,
    projectBudgetList,

    fetchProjectList,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
  }
})
