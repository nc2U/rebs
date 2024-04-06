import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import type {
  IssueProject,
  ProjectFilter,
  Member,
  Role,
  Tracker,
  IssueStatus,
  CodeValue,
  Issue,
  IssueComment,
  TimeEntry,
  TimeEntryFilter,
  IssueLogEntry,
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
  const fetchIssueProjectList = async (payload: ProjectFilter) => {
    console.log(payload)
    let url = `/issue-project/?parent__isnull=1`
    url += `&status=${payload?.status ?? '1'}`

    return await api
      .get(url)
      .then(res => (issueProjectList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

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
      .get(`/tracker/`)
      .then(res => (trackerList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // status states & getters
  const statusList = ref<IssueStatus[]>([])

  const fetchStatusList = () =>
    api
      .get(`/issue-status/`)
      .then(res => (statusList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // code-activity states & getters
  const activityList = ref<CodeValue[]>([])

  const fetchActivityList = () =>
    api
      .get(`/code-activity/`)
      .then(res => (activityList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // code-priority states & getters
  const priorityList = ref<CodeValue[]>([])

  const fetchPriorityList = () =>
    api
      .get(`/code-priority/`)
      .then(res => (priorityList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // issue states & getters
  const issue = ref<Issue | null>(null)
  const issueList = ref<Issue[]>([])
  const getIssues = computed(() =>
    issueList.value.map(i => ({
      value: i.pk,
      label: i.subject,
    })),
  )

  const fetchIssue = (pk: number) =>
    api
      .get(`/issue/${pk}/`)
      .then(res => (issue.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchIssueList = async (payload: { status__closed?: '1' | '0' | ''; project?: string }) => {
    let url = `/issue/?1=1`
    if (payload.status__closed) url += `&status__closed=${payload.status__closed}`
    if (payload.project) url += `&project__slug=${payload.project}`

    return await api
      .get(url)
      .then(res => (issueList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const createIssue = (payload: any) =>
    api
      .post(`/issue/`, payload)
      .then(async res => {
        await fetchIssue(res.data.pk)
        await fetchIssueList({ status__closed: '', project: res.data.project.slug })
        await fetchIssueLogList({ issue: res.data.pk })
        await fetchIssueCommentList({ issue: res.data.pk })
        await fetchTimeEntryList({ issue: res.data.pk })
        message()
      })
      .catch(err => errorHandle(err.response.data))

  const updateIssue = (payload: any) =>
    api
      .put(`/issue/${payload.pk}/`, payload)
      .then(async () => {
        await fetchIssue(payload.pk)
        await fetchIssueLogList({ issue: payload.pk })
        await fetchIssueLogList({ issue: payload.pk })
        await fetchIssueCommentList({ issue: payload.pk })
        await fetchTimeEntryList({ issue: payload.pk })
        message()
      })
      .catch(err => errorHandle(err.response.data))

  const patchIssue = (payload: any) =>
    api
      .patch(`/issue/${payload.pk}/`, payload)
      .then(() =>
        fetchIssue(payload.pk).then(() =>
          fetchIssueLogList({ issue: payload.pk }).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteIssue = (pk: number) =>
    api
      .delete(`/issue/${pk}/`)
      .then(() =>
        fetchIssueList({}).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // issue-comment states & getters
  const issueComment = ref<IssueComment | null>(null)
  const issueCommentList = ref<IssueComment[]>([])

  const fetchIssueComment = (pk: number) =>
    api
      .get(`/issue-comment/${pk}/`)
      .then(res => (issueComment.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchIssueCommentList = async (payload: any) => {
    let url = `/issue-comment/?1=1`
    if (payload.issue) url += `&issue=${payload.issue}`
    if (payload.user) url += `&user=${payload.user}`

    return await api
      .get(url)
      .then(res => (issueCommentList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const updateIssueComment = (payload: any) =>
    api
      .put(`/issue-comment/${payload.pk}/`, payload)
      .then(() =>
        fetchIssueComment(payload.pk).then(() =>
          fetchIssueCommentList({ issue: payload.issue }).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteIssueComment = (pk: number, issue: number) =>
    api
      .delete(`/issue-comment/${pk}/`)
      .then(() =>
        fetchIssueCommentList({ issue }).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // time-entry states & getters
  const timeEntry = ref<TimeEntry | null>(null)
  const timeEntryList = ref<TimeEntry[]>([])

  const fetchTimeEntry = (pk: number) =>
    api
      .get(`/time-entry/${pk}/`)
      .then(res => (timeEntry.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchTimeEntryList = async (payload: TimeEntryFilter) => {
    let url = `/time-entry/?1=1`
    if (payload.project) url += `&issue__project__slug=${payload.project}`
    if (payload.issue) url += `&issue=${payload.issue}`
    if (payload.user) url += `&user=${payload.user}`
    if (payload.activity) url += `&activity=${payload.activity}`
    if (payload.hours) url += `&hours=${payload.hours}`
    if (payload.from_spent_on) url += `&from_spent_on=${payload.from_spent_on}`
    if (payload.to_spent_on) url += `&to_spent_on=${payload.to_spent_on}`
    if (payload.issue__tracker) url += `&issue__tracker=${payload.issue__tracker}`
    if (payload.issue__parent) url += `&issue__parent=${payload.issue__parent}`
    if (payload.issue__status) url += `&issue__status=${payload.issue__status}`
    if (payload.issue__fixed_version) url += `&issue__fixed_version=${payload.issue__fixed_version}`
    if (payload.issue__category) url += `&issue__category=${payload.issue__category}`

    return await api
      .get(url)
      .then(res => (timeEntryList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const createTimeEntry = (payload: TimeEntry) =>
    api
      .post(`/time-entry/`, payload)
      .then(res =>
        fetchTimeEntry(res.data.pk).then(() => fetchTimeEntryList({}).then(() => message())),
      )
      .catch(err => errorHandle(err.response.data))

  const updateTimeEntry = (payload: TimeEntry) =>
    api
      .put(`/time-entry/${payload.pk}/`, payload)
      .then(() =>
        fetchTimeEntry(payload.pk).then(() => fetchTimeEntryList({}).then(() => message())),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteTimeEntry = (pk: number) =>
    api
      .delete(`/time-entry/${pk}/`)
      .then(() =>
        fetchTimeEntryList({}).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // activity-log states & getters
  const activityLogList = ref<any[]>([])
  const groupedActivities = computed(() => {
    return activityLogList.value.reduce((result, currentValue) => {
      ;(result[currentValue['act_date']] = result[currentValue['act_date']] || []).push(
        currentValue,
      )
      return result
    }, {})
  })

  const fetchActivityLogList = async (payload: any) => {
    let url = `/act-entry/?1=1`
    if (payload.sort) url += `&sort=${payload.sort}`
    if (payload.action) url += `&action=${payload.action}`
    if (payload.project) url += `&project__slug=${payload.project}`
    if (payload.issue) url += `&issue=${payload.issue}`
    if (payload.issue__isnull) url += `&issue__isnull=${payload.issue__isnull}`
    if (payload.change_sets_isnull) url += `&change_sets_isnull=${payload.change_sets_isnull}`
    if (payload.news__isnull) url += `&news__isnull=${payload.news__isnull}`
    if (payload.document__isnull) url += `&document__isnull=${payload.document__isnull}`
    if (payload.file__isnull) url += `&file__isnull=${payload.file__isnull}`
    if (payload.wiki__isnull) url += `&wiki__isnull=${payload.wiki__isnull}`
    if (payload.message__isnull) url += `&message__isnull=${payload.message__isnull}`
    if (payload.spent_time__isnull) url += `&spent_time__isnull=${payload.spent_time__isnull}`
    if (payload.act_date) url += `&act_date=${payload.act_date}`
    if (payload.from_act_date) url += `&from_act_date=${payload.from_act_date}`
    if (payload.to_act_date) url += `&to_act_date=${payload.to_act_date}`
    if (payload.user) url += `&user=${payload.user}`
    return await api
      .get(url)
      .then(res => (activityLogList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  // activity-log states & getters
  const issueLogList = ref<IssueLogEntry[]>([])

  const fetchIssueLogList = async (payload: { issue?: number; user?: number }) => {
    let url = `/log-entry/?1=1`
    if (payload.issue) url += `&issue=${payload.issue}`
    if (payload.user) url += `&user=${payload.user}`
    return await api
      .get(url)
      .then(res => (issueLogList.value = res.data.results))
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
    getIssues,
    fetchIssue,
    fetchIssueList,
    createIssue,
    updateIssue,
    patchIssue,
    deleteIssue,

    issueComment,
    issueCommentList,
    fetchIssueComment,
    fetchIssueCommentList,
    updateIssueComment,
    deleteIssueComment,

    timeEntry,
    timeEntryList,
    fetchTimeEntry,
    fetchTimeEntryList,
    createTimeEntry,
    updateTimeEntry,
    deleteTimeEntry,

    activityLogList,
    groupedActivities,
    fetchActivityLogList,

    issueLogList,
    fetchIssueLogList,
  }
})
