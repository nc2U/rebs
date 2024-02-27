export interface TaskProject {
  pk?: number
  company: number
  name: string
  description: string
  homepage: string | null
  is_public: boolean
  parent: number | null
  slug: string
  status: '1' | '9'
  is_inherit_members: boolean
  depth: number
  sub_projects?: TaskProject[]
  module: Module | null
  user?: number
  created?: string
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
