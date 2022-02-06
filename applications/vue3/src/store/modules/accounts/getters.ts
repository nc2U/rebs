import { AccountsState } from './state'

const getters = {
  isAuthorized(state: AccountsState) {
    return state.accessToken.length && !!state.userInfo
  },

  staffAuth(state: AccountsState) {
    return state.userInfo?.staffauth?.is_staff || state.userInfo?.is_superuser
  },

  superAuth(state: AccountsState) {
    return state.userInfo?.is_superuser
  },
  initComId(): number {
    return 1
  },
  initProjId(state: AccountsState) {
    return state.userInfo?.staffauth?.assigned_project
      ? state.userInfo?.staffauth?.assigned_project
      : state.userInfo?.staffauth?.allowed_projects[0]
  },
  myTodos: (state: AccountsState) => {
    return state.todoList.filter(
      (todo) => !todo.soft_deleted && todo.user == state.userInfo?.pk,
    )
  },
}

export default getters
