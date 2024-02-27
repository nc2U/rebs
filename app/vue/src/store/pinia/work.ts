import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import type { TaskProject } from '@/store/types/work'

export const useWork = defineStore('work', () => {
  // states & getters
  const taskProjectList = ref<TaskProject[]>([])
  const taskProject = ref<TaskProject | null>(null)
  const AllTaskProjects = computed(() => {
    const result: TaskProject[] = []

    function flatten(proj: TaskProject) {
      result.push(proj)
      if (!!proj.sub_projects?.length) {
        proj.sub_projects.forEach(sub => {
          flatten(sub)
        })
      }
    }

    taskProjectList.value.forEach(root => {
      flatten(root)
    })
    return result
  })

  // actions
  const fetchTaskProjectList = () =>
    api
      .get('/issue-project/?parent__isnull=true')
      .then(res => (taskProjectList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchTaskProject = (slug: string) =>
    api
      .get(`/issue-project/${slug}/`)
      .then(res => (taskProject.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createTaskProject = (payload: TaskProject) =>
    api
      .post(`/issue-project/`, payload)
      .then(res => {
        fetchTaskProject(res.data.slug).then(() => message())
      })
      .catch(err => errorHandle(err.response.data))

  const updateTaskProject = (payload: TaskProject) =>
    api
      .put(`/issue-project/${payload.slug}/`, payload)
      .then(res => fetchTaskProject(res.data.slug).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteTaskProject = (pk: number) =>
    api
      .delete(`/issue-project/${pk}/`)
      .then(() =>
        fetchTaskProjectList().then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  return {
    taskProjectList,
    AllTaskProjects,
    taskProject,

    fetchTaskProjectList,
    fetchTaskProject,
    createTaskProject,
    updateTaskProject,
    deleteTaskProject,
  }
})
