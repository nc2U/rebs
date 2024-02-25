export interface TaskProject {
  pk?: number
  company: number
  name: string
  desc: string
  identifier: string
  homepage: string | null
  is_public: boolean
  parent_project: number | null
  depth: number
  is_inherit_members: boolean
  sub_projects?: TaskProject[]
  created?: string
  user?: number
  module: Module | null
}

export interface Module {
  pk?: number
  issue: boolean
  time: boolean
  news: boolean
  document: boolean
  file: boolean
  wiki: boolean
  repository: boolean
  forum: boolean
  calendar: boolean
  gantt: boolean
  project: number
}
