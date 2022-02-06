export declare interface StaffAuth {
  pk: number
  is_staff: boolean
  assigned_project: number
  allowed_projects: number[]
  contract: string
  payment: string
  notice: string
  project_cash: string
  project_docs: string
  human_resource: string
  company_settings: string
  auth_manage: string
}

interface Todo {
  pk: number
  title: string
  completed: boolean
  soft_deleted: boolean
}

export declare interface User {
  pk: number
  email: string
  username: string
  is_active: boolean
  date_joined: string
  is_superuser: boolean
  staffauth: StaffAuth | null
  todos: Todo[]
}

export declare interface LockedUser {
  pk: number
  email: string
  username: string
}

export declare interface AccountsState {
  accessToken: string
  userInfo: User | null
  lockedUser: LockedUser | null
}

const state: AccountsState = {
  accessToken: '',
  userInfo: null,
  lockedUser: null,
}

export default state
