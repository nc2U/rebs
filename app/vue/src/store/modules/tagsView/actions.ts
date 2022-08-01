const actions = {
  addView({ dispatch }: any, view: any) {
    dispatch('addVisitedView', view)
    dispatch('addCachedView', view)
  },

  addVisitedView({ commit }: any, view: any) {
    commit('ADD_VISITED_VIEW', view)
  },
  addCachedView({ commit }: any, view: any) {
    commit('ADD_CACHED_VIEW', view)
  },

  delView({ dispatch, state }: any, view: any) {
    return new Promise(resolve => {
      dispatch('delVisitedView', view)
      dispatch('delCachedView', view)
      resolve({
        visitedViews: [...state.visitedViews],
        cachedViews: [...state.cachedViews],
      })
    })
  },
  delVisitedView({ commit, state }: any, view: any) {
    return new Promise(resolve => {
      commit('DEL_VISITED_VIEW', view)
      resolve([...state.visitedViews])
    })
  },
  delCachedView({ commit, state }: any, view: any) {
    return new Promise(resolve => {
      commit('DEL_CACHED_VIEW', view)
      resolve([...state.cachedViews])
    })
  },

  delOthersViews({ dispatch, state }: any, view: any) {
    return new Promise(resolve => {
      dispatch('delOthersVisitedViews', view)
      dispatch('delOthersCachedViews', view)
      resolve({
        visitedViews: [...state.visitedViews],
        cachedViews: [...state.cachedViews],
      })
    })
  },
  delOthersVisitedViews({ commit, state }: any, view: any) {
    return new Promise(resolve => {
      commit('DEL_OTHERS_VISITED_VIEWS', view)
      resolve([...state.visitedViews])
    })
  },
  delOthersCachedViews({ commit, state }: any, view: any) {
    return new Promise(resolve => {
      commit('DEL_OTHERS_CACHED_VIEWS', view)
      resolve([...state.cachedViews])
    })
  },

  delAllViews({ dispatch, state }: any, view: any) {
    return new Promise(resolve => {
      dispatch('delAllVisitedViews', view)
      dispatch('delAllCachedViews', view)
      resolve({
        visitedViews: [...state.visitedViews],
        cachedViews: [...state.cachedViews],
      })
    })
  },
  delAllVisitedViews({ commit, state }: any) {
    return new Promise(resolve => {
      commit('DEL_ALL_VISITED_VIEWS')
      resolve([...state.visitedViews])
    })
  },
  delAllCachedViews({ commit, state }: any) {
    return new Promise(resolve => {
      commit('DEL_ALL_CACHED_VIEWS')
      resolve([...state.cachedViews])
    })
  },

  updateVisitedView({ commit }: any, view: any) {
    commit('UPDATE_VISITED_VIEW', view)
  },
}

export default actions
