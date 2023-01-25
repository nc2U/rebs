export declare interface User {
  pk?: number
  email: string
  username: string
  is_active: boolean
  is_superuser: boolean
  date_joined: string
  staffauth: StaffAuth | null
  profile: Profile | null
  todos: Todo[]
}

interface StaffAuth {
  pk?: number
  company: number
  is_staff: boolean
  assigned_project: number
  allowed_projects: number[]
  contract: string
  payment: string
  notice: string
  project: string
  project_cash: string
  project_docs: string
  human_resource: string
  company_settings: string
  company_cash: string
  company_docs: string
  auth_manage: string
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
