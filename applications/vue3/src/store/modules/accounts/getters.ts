import { AccountsState } from './state'

const getters = {
  isAuthorized(state: AccountsState) {
    return state.accessToken.length && !!state.userInfo
  },

  staffAuth(state: AccountsState) {
    return state.userInfo?.staffauth?.is_staff || state.userInfo?.is_superuser
      ? state.userInfo.staffauth
      : null
  },

  superAuth(state: AccountsState) {
    return state.userInfo?.is_superuser
  },
  initComId(state: AccountsState): number {
    return state.userInfo?.staffauth?.company
      ? state.userInfo.staffauth.company
      : 1
  },
  initProjId(state: AccountsState) {
    return state.userInfo?.staffauth?.assigned_project
      ? state.userInfo?.staffauth?.assigned_project
      : state.userInfo?.staffauth?.allowed_projects[0]
  },
  myTodos: (state: AccountsState) => {
    const pk = state.userInfo?.pk
    return pk
      ? state.todoList.filter(todo => !todo.soft_deleted && todo.user === pk)
      : []
  },
}

export default getters
