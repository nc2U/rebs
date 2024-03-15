interface BCParent {
  pk: number
  name: string
  slug: string
}

export interface SimpleMember {
  pk: number
  user: { pk: number; username: string }
  roles: { pk: number; name: string }[]
  add_roles?: { pk: number; name: string }[]
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
  parent_members: SimpleMember[]
  members: SimpleMember[]
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

export interface Member {
  pk: number
  user: number
  roles: number[]
}

export interface Issue {
  pk: number
  project: { slug: string; name: string }
  tracker: string
  status: string
  priority: string
  subject: string
  description: string
  category: number | null
  fixed_version: number | null
  assigned_to: { pk: number; username: string } | null
  parent: number | null
  watchers: number[]
  is_private: boolean
  estimated_hours: number | null
  start_date: string | null
  due_date: string | null
  done_ratio: number
  closed: string | null
  creator: number
  updater: number | null
  created: string
  updated: string
}
