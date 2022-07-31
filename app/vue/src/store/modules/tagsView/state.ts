import { State } from '@/store'

interface VisitedViews {
  fullPath: string
  name: string
  path: string
  title: string
  meta: {
    affix: string
    icon: string
    title: string
  }
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
