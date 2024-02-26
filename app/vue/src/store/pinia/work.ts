import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import type { TaskProject } from '@/store/types/work'

export const useWork = defineStore('work', () => {
  // states & getters
  const taskProjectList = ref<TaskProject[]>([])
  const AllTaskProjects = ref<TaskProject[]>([])
  const taskProject = ref<TaskProject | null>(null)

  // actions
  const fetchTaskProjectList = () =>
    api
      .get('/task-project/?parent__isnull=true')
      .then(res => (taskProjectList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchAllTaskProjects = () =>
    api
      .get('/task-project/')
      .then(res => (AllTaskProjects.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchTaskProject = (slug: string) =>
    api
      .get(`/task-project/${slug}/`)
      .then(res => (taskProject.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createTaskProject = (payload: TaskProject) =>
    api
      .post(`/task-project/`, payload)
      .then(res => {
        fetchTaskProject(res.data.identifier).then(() => message())
      })
      .catch(err => errorHandle(err.response.data))

  const updateTaskProject = (payload: TaskProject) =>
    api
      .put(`/task-project/${payload.slug}/`, payload)
      .then(res => fetchTaskProject(res.data.slug).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteTaskProject = (pk: number) =>
    api
      .delete(`/task-project/${pk}/`)
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
    fetchAllTaskProjects,
    fetchTaskProject,
    createTaskProject,
    updateTaskProject,
    deleteTaskProject,
  }
})
