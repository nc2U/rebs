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
  const getTaskProjects = computed(() =>
    taskProjectList.value.map(p => ({
      value: p.pk,
      label: p.name,
      depth: p.depth,
      subs: p.sub_projects?.map(s1 => ({
        value: s1.pk,
        label: s1.name,
        depth: s1.depth,
        subs: s1.sub_projects?.map(s2 => ({
          value: s2.pk,
          label: s2.name,
          depth: s2.depth,
          subs: s2.sub_projects?.map(s3 => ({
            value: s3.pk,
            label: s3.name,
            depth: s3.depth,
            subs: s3.sub_projects?.map(s4 => ({
              value: s4.pk,
              label: s4.name,
              depth: s4.depth,
              subs: s4.sub_projects?.map(s5 => ({
                value: s5.pk,
                label: s5.name,
                depth: s5.depth,
              })),
            })),
          })),
        })),
      })),
    })),
  )

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
    getTaskProjects,

    fetchTaskProjectList,
    fetchAllTaskProjects,
    fetchTaskProject,
    createTaskProject,
    updateTaskProject,
    deleteTaskProject,
  }
})
