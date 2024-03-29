import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import type {
  IssueProject,
  Member,
  Role,
  Issue,
  Tracker,
  IssueStatus,
  CodeValue,
  LogEntry,
} from '@/store/types/work'

export const useWork = defineStore('work', () => {
  // Issue Project states & getters
  const issueProject = ref<IssueProject | null>(null)
  const issueProjectList = ref<IssueProject[]>([])
  const AllIssueProjects = computed(() => {
    const result: IssueProject[] = []

    function flatten(proj: IssueProject) {
      result.push(proj)
      if (!!proj.sub_projects?.length) proj.sub_projects.forEach(sub => flatten(sub))
    }

    issueProjectList.value.forEach(rootProj => flatten(rootProj))
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

  const patchIssueProject = async (payload: {
    slug: string
    users: number[]
    roles: number[]
    del_mem?: number
  }) => {
    const type = payload.del_mem ? 'warning' : 'success'
    return await api
      .patch(`/issue-project/${payload.slug}/`, payload)
      .then(res => fetchIssueProject(res.data.slug).then(() => message(type)))
      .catch(err => errorHandle(err.response.data))
  }

  const deleteIssueProject = (pk: number) =>
    api
      .delete(`/issue-project/${pk}/`)
      .then(() =>
        fetchIssueProjectList().then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // Role & Permission states & getters
  const role = ref<Role | null>(null)
  const roleList = ref<Role[]>([])

  const fetchRole = (pk: number) =>
    api
      .get(`/role/${pk}/`)
      .then(res => (role.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchRoleList = () =>
    api
      .get(`/role/`)
      .then(res => (roleList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // member states & getters
  const member = ref<Member | null>(null)
  const memberList = ref<Member[]>([])

  const fetchMember = (pk: number) =>
    api
      .get(`/member/${pk}/`)
      .then(res => (member.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchMemberList = () =>
    api
      .get(`/member/`)
      .then(res => (memberList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const patchMember = (payload: { pk: number; user?: number; roles?: number[]; slug: string }) =>
    api
      .patch(`/member/${payload.pk}/`, payload)
      .then(res =>
        fetchIssueProject(payload.slug).then(() => fetchMember(res.data.pk).then(() => message())),
      )
      .catch(err => errorHandle(err.response.data))

  // tracker states & getters
  const trackerList = ref<Tracker[]>([])

  const fetchTrackerList = () =>
    api
      .get(`tracker`)
      .then(res => (trackerList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // status states & getters
  const statusList = ref<IssueStatus[]>([])

  const fetchStatusList = () =>
    api
      .get(`issue-status`)
      .then(res => (statusList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // code-activity states & getters
  const activityList = ref<CodeValue[]>([])

  const fetchActivityList = () =>
    api
      .get(`code-activity`)
      .then(res => (activityList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // code-priority states & getters
  const priorityList = ref<CodeValue[]>([])

  const fetchPriorityList = () =>
    api
      .get(`code-priority`)
      .then(res => (priorityList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // issue states & getters
  const issue = ref<Issue | null>(null)
  const issueList = ref<Issue[]>([])

  const fetchIssue = (pk: number) =>
    api
      .get(`/issue/${pk}/`)
      .then(res => (issue.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchIssueList = () =>
    api
      .get(`/issue/`)
      .then(res => (issueList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createIssue = (payload: any) =>
    api
      .post(`/issue/`, payload)
      .then(res => fetchIssue(res.data.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const updateIssue = (payload: any) =>
    api
      .put(`/issue/${payload.pk}/`, payload)
      .then(() => fetchIssue(payload.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const patchIssue = (payload: any) =>
    api
      .patch(`/issue/${payload.pk}/`, payload)
      .then(() => fetchIssue(payload.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteIssue = (pk: number) =>
    api
      .delete(`/issue/${pk}/`)
      .then(() =>
        fetchIssueList().then(() => message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.')),
      )
      .catch(err => errorHandle(err.response.data))

  // issue states & getters
  const logEntryList = ref<LogEntry[]>([])

  const fetchLogEntryList = async (payload: { issue: string; user?: number }) => {
    let url = `/log-entry/?issue=${payload.issue}`
    if (payload.user) url += `&user=${payload.user}`
    return await api
      .get(url)
      .then(res => (logEntryList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  return {
    issueProject,
    issueProjectList,
    AllIssueProjects,
    fetchIssueProjectList,
    fetchIssueProject,
    createIssueProject,
    updateIssueProject,
    patchIssueProject,
    deleteIssueProject,

    role,
    roleList,
    fetchRole,
    fetchRoleList,

    member,
    memberList,
    fetchMember,
    fetchMemberList,
    patchMember,

    trackerList,
    fetchTrackerList,

    statusList,
    fetchStatusList,

    activityList,
    fetchActivityList,

    priorityList,
    fetchPriorityList,

    issue,
    issueList,
    fetchIssue,
    fetchIssueList,
    createIssue,
    updateIssue,
    patchIssue,
    deleteIssue,

    logEntryList,
    fetchLogEntryList,
  }
})
