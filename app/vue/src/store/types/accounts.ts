export declare interface User {
  pk?: number
  email: string
  username: string
  is_active: boolean
  is_superuser: boolean
  date_joined: string
  staffauth: StaffAuth | null
  profile: number | null
}

type Auth = '0' | '1' | '2'

export interface StaffAuth {
  pk?: number
  company: number | null
  is_staff: boolean
  assigned_project: number | null
  allowed_projects: number[]
  contract: Auth
  payment: Auth
  notice: Auth
  project_cash: Auth
  project_docs: Auth
  project: Auth
  company_cash: Auth
  company_docs: Auth
  human_resource: Auth
  company_settings: Auth
  auth_manage: Auth
}

export type Profile = {
  [key: string]: undefined | number | null | string
  pk?: number | null
  user: number | null
  name: string
  birth_date: string
  cell_phone: string
}

export interface Todo {
  pk?: number
  user?: number
  title?: string
  completed?: boolean
  soft_deleted?: boolean
}
