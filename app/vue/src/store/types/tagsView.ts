export interface VisitedView {
  name: string
  path: string
  fullPath: string
  meta: Meta
}

export interface Meta {
  title?: string
  auth?: boolean
  affix?: boolean
  noCache?: boolean
}

export type CachedViews = {
  [key: number]: string
}
