import { State } from '@/store'

interface Meta {
  title: string
  affix: boolean
}

export interface VisitedViews {
  name: string
  path: string
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
