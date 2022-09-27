export interface Group {
  pk: number | null
  name: string
  manager: number[]
}

export interface Board {
  pk: number | null
  group: number | null
  name: string
  order: number | null
  search_able: boolean
  manager: number[]
}

export interface Category {
  pk: number | null
  board: number | null
  name: string
  parent: number | null
  order: number | null
}

export interface SuitCase {
  pk: number | null
  project: number | null
  sort: '1' | '2' | '3' | '4' | '5'
  level: '0' | '1' | '2' | '3'
  related_case: number | null
  court: string
  other_agency: string
  case_number: string
  case_name: string
  plaintiff: string
  defendant: string
  related_debtor: string
  case_start_date: string
  summary: string
}

export interface SimpleSuitCase {
  pk: number | null
  __str__: string
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
  lawsuit_name?: string | null
  title: string
  execution_date: string | null
  content: string
  is_hide_comment: boolean
  hit: number
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
  post: number
  link: string
  hit: number
  del?: boolean
}

export interface Image {
  pk: null | number
  post: number
  image: string
  del?: boolean
}

export interface AFile {
  pk: null | number
  post?: number
  file: string
  newFile?: string
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
  like?: number[]
  dislike?: number[]
  blame?: number
  secret?: boolean
  password?: string
  soft_delete?: string | null
}
