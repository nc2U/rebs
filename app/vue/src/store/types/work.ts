interface BCParent {
  pk: number
  name: string
  slug: string
}

export interface IssueProject {
  pk?: number
  company: number
  name: string
  description: string
  homepage: string | null
  is_public: boolean
  family_tree: BCParent[]
  parent: number | null
  slug: string
  status: '1' | '9'
  is_inherit_members: boolean
  depth: number
  members: number[]
  sub_projects?: IssueProject[]
  trackers: number[]
  module: Module | null
  user?: number
  created?: string
}

export interface Module {
  pk?: number
  project: number
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
}

export interface Role {
  pk: number
  name: string
  assignable: boolean
  issue_visible: 'ALL' | 'PUB' | 'PRI'
  time_entry_visible: 'ALL' | 'PRI'
  user_visible: 'ALL' | 'PRJ'
  default_time_activity: number | null
  order: number
  user: number
  created: string
  updated: string
}
