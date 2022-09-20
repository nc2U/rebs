export interface Post {
  pk: number | null
  board: number | null
  is_notice: boolean
  project: number | null
  proj_name?: string | null
  category: number | null
  cate_name?: string | null
  lawsuit: number | null
  title: string
  execution_date: string | null
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
  links: Link[]
  images: Image[]
  files: File[]
  comments?: number[]
  user?: number | null
  soft_delete?: string | null
  created?: string
  updated?: string
  is_new?: boolean
}

interface Link {
  pk: null | number
  link: string
  hit: number
}

interface Image {
  pk: null | number
  image: string
}

interface File {
  pk: null | number
  file: string
  hit: number
}

export interface PatchPost {
  pk: number
  is_notice?: boolean
  category?: number | null
  lawsuit?: number | null
  title?: string
  execution_date?: string | null
  content?: string
  is_hide_comment?: boolean
  hit?: number
  like?: number
  dislike?: number
  blame?: number
  secret?: boolean
  password?: string
  soft_delete?: string | null
}
