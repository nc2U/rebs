export interface TaskProject {
  pk: number
  company: number
  name: string
  desc: string
  identifier: string
  homepage: string | null
  is_public: boolean
  parent_project: number | null
  is_inherit_members: boolean
  sub_projects: TaskProject[]
  created: string
  user: number
}
