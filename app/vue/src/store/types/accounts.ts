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

export interface StaffAuth {
  pk?: number
  company: number
  is_staff: boolean
  assigned_project: number | null
  allowed_projects: number[]
  contract: '0' | '1' | '2'
  payment: '0' | '1' | '2'
  notice: '0' | '1' | '2'
  project_cash: '0' | '1' | '2'
  project_docs: '0' | '1' | '2'
  project: '0' | '1' | '2'
  company_cash: '0' | '1' | '2'
  company_docs: '0' | '1' | '2'
  human_resource: '0' | '1' | '2'
  company_settings: '0' | '1' | '2'
  auth_manage: '0' | '1' | '2'
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
