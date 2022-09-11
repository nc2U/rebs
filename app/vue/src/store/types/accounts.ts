export declare interface User {
  pk?: number
  email: string
  username: string
  is_active: boolean
  date_joined: string
  is_superuser: boolean
  staffauth: StaffAuth | null
  profile: Profile | null
  todos: Todo[]
}

export type Profile = {
  [key: string]: number | null | string | Blob | undefined
  pk?: number | null
  user: number | null
  name: string
  birth_date: string
  cell_phone: string
}

export declare interface Todo {
  pk?: number
  url: string
  user: number
  title: string
  completed: boolean
  soft_deleted: boolean
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
