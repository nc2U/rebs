import { AccountsState } from './state'

const getters = {
  superAuth(state: AccountsState) {
    return state.userInfo?.is_superuser
  },
  staffAuth(state: AccountsState) {
    return state.userInfo?.staffauth ? state.userInfo.staffauth : null
  },
  isAuthorized(state: AccountsState) {
    return state.accessToken.length && !!state.userInfo
  },
  initComId(state: AccountsState): number {
    return state.userInfo?.staffauth?.company
      ? state.userInfo.staffauth.company
      : 1
  },
  initProjId(state: AccountsState) {
    return state.userInfo?.staffauth?.assigned_project
      ? state.userInfo?.staffauth?.assigned_project
      : state.userInfo?.staffauth?.allowed_projects[0] || 0
  },
  myTodos: (state: AccountsState) => {
    const pk = state.userInfo?.pk
    return pk
      ? state.todoList.filter(todo => !todo.soft_deleted && todo.user === pk)
      : []
  },
}

export default getters
