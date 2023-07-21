export interface Meta {
  title: string
  affix: boolean
  noCache: boolean
}

export interface VisitedViews {
  name: string
  path: string
  fullPath: string
  query?: { [key: string]: string }
  meta: Meta
}

export type CachedViews = {
  [key: number]: string
}
