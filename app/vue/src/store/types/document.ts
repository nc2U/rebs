export interface Category {
  pk: number | null
  board: number | null
  name: string
  parent: number | null
  order: number | null
}

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
  links?: Link[]
  images?: Image[]
  files?: File[]
  comments?: number[]
  user?: number | null
  soft_delete?: string | null
  created?: string
  updated?: string
  is_new?: boolean
}

export interface Link {
  pk: null | number
  link: string
  hit: number
  del?: boolean
}

export interface Image {
  pk: null | number
  image: string
  del?: boolean
}

export interface File {
  pk: null | number
  file: string
  oldFile?: string
  hit: number
  del?: boolean
}

export type Attatches = {
  oldLinks: Link[]
  oldImages?: Image[]
  oldFiles: File[]

  newLinks: Link[]
  newImages?: Image[]
  newFiles: File[]
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
