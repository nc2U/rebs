export declare interface StaffAuth {
  id: number
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

export declare interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  date_joined: string
  is_superuser: boolean
  staffauth: StaffAuth | null
}

export declare interface LockedUser {
  id: number
  email: string
  username: string
}

export declare interface AccountsState {
  accessToken: string
  userInfo: User | null
}

const state: AccountsState = {
  accessToken: '',
  userInfo: null,
}

export default state
