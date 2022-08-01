import { TagsViewState } from '@/store/modules/tagsView/state'

const mutations = {
  ADD_VISITED_VIEW: (state: TagsViewState, view: any) => {
    if (state.visitedViews.some(v => v.name === view.name)) return
    // state.visitedViews.push(
    //   Object.assign({}, view, {
    //     title: view.meta.title || 'no-name',
    //   }),
    // )
  },
  ADD_CACHED_VIEW: (state: TagsViewState, view: any) => {
    if (state.cachedViews.includes(view.name)) return
    if (!view.meta.noCache) {
      state.cachedViews.push(view.name)
    }
  },

  DEL_VISITED_VIEW: (state: TagsViewState, view: any) => {
    for (const [i, v] of state.visitedViews.entries()) {
      if (v.path === view.path) {
        state.visitedViews.splice(i, 1)
        break
      }
    }
  },
  DEL_CACHED_VIEW: (state: TagsViewState, view: any) => {
    const index = state.cachedViews.indexOf(view.name)
    index > -1 && state.cachedViews.splice(index, 1)
  },

  DEL_OTHERS_VISITED_VIEWS: (state: TagsViewState, view: any) => {
    state.visitedViews = state.visitedViews.filter(v => {
      return v.meta.affix || v.path === view.path
    })
  },
  DEL_OTHERS_CACHED_VIEWS: (state: TagsViewState, view: any) => {
    const index = state.cachedViews.indexOf(view.name)
    if (index > -1) {
      state.cachedViews = state.cachedViews.slice(index, index + 1)
    } else {
      // if index = -1, there is no cached tags
      state.cachedViews = []
    }
  },

  DEL_ALL_VISITED_VIEWS: (state: TagsViewState) => {
    // keep affix tags
    const affixTags = state.visitedViews.filter(tag => tag.meta.affix)
    state.visitedViews = affixTags
  },
  DEL_ALL_CACHED_VIEWS: (state: TagsViewState) => {
    state.cachedViews = []
  },

  UPDATE_VISITED_VIEW: (state: TagsViewState, view: any) => {
    for (let v of state.visitedViews) {
      if (v.path === view.path) {
        v = Object.assign(v, view)
        break
      }
    }
  },
}

export default mutations
