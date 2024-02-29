import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import type { IssueProject } from '@/store/types/work'

export const useWork = defineStore('work', () => {
  // states & getters
  const issueProjectList = ref<IssueProject[]>([])
  const issueProject = ref<IssueProject | null>(null)
  const AllIssueProjects = computed(() => {
    const result: IssueProject[] = []

    function flatten(proj: IssueProject) {
      result.push(proj)
      if (!!proj.sub_projects?.length) {
        proj.sub_projects.forEach(sub => {
          flatten(sub)
        })
      }
    }

    issueProjectList.value.forEach(root => {
      flatten(root)
    })
    return result
  })

  // actions
  const fetchIssueProjectList = () =>
    api
      .get('/issue-project/?parent__isnull=true')
      .then(res => (issueProjectList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchIssueProject = (slug: string) =>
    api
      .get(`/issue-project/${slug}/`)
      .then(res => (issueProject.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createIssueProject = (payload: IssueProject) =>
    api
      .post(`/issue-project/`, payload)
      .then(res => {
        fetchIssueProject(res.data.slug).then(() => message())
      })
      .catch(err => errorHandle(err.response.data))

  const updateIssueProject = (payload: IssueProject) =>
    api
      .put(`/issue-project/${payload.slug}/`, payload)
      .then(res => fetchIssueProject(res.data.slug).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteIssueProject = (pk: number) =>
    api
      .delete(`/issue-project/${pk}/`)
      .then(() =>
        fetchIssueProjectList().then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  return {
    issueProjectList,
    AllIssueProjects,
    issueProject,

    fetchIssueProjectList,
    fetchIssueProject,
    createIssueProject,
    updateIssueProject,
    deleteIssueProject,
  }
})
