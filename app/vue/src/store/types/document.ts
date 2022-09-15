export interface Post {
  pk: number
  board: number
  is_notice: boolean
  project: number
  project_name?: string | null
  category: number | null
  lawsuit: number | null
  title: string
  execution_date: string
  content: string
  is_hide_comment: boolean
  hit: number
  like: number
  dislike: number
  blame: number
  ip: string | null
  device: string
  secret: boolean
  password: string
  user: number | null
  soft_delete: string | null
  created: string
  updated: string
}
