interface Meta {
  title: string
  affix: boolean
  noCache: boolean
}

export interface VisitedViews {
  fullPath: string
  path: string
  name: string
  meta: Meta
}

export type CachedViews = {
  [key: number]: string
}
