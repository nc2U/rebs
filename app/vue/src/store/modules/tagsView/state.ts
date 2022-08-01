import { State } from '@/store'

interface Meta {
  title: string
  affix: boolean
}

export interface VisitedViews {
  fullPath: string
  path: string
  name: string
  meta: Meta
}

interface CachedViews {
  [key: number]: 'string'
}

export declare interface TagsViewState extends State {
  visitedViews: VisitedViews[]
  cachedViews: CachedViews[]
}

const state: TagsViewState = {
  visitedViews: [],
  cachedViews: [],
}

export default state
