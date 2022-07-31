const actions = {
  addView({ dispatch }: any, view: any) {
    dispatch('addVisitedView', view)
    dispatch('addCachedView', view)
  },

  // addVisitedView({ commit }, view) {
  //   commit('ADD_VISITED_VIEW', view)
  // },
  // addCachedView({ commit }, view) {
  //   commit('ADD_CACHED_VIEW', view)
  // },
  //
  // delView({ dispatch, state }, view) {
  //   return new Promise(resolve => {
  //     dispatch('delVisitedView', view)
  //     dispatch('delCachedView', view)
  //     resolve({
  //       visitedViews: [...state.visitedViews],
  //       cachedViews: [...state.cachedViews],
  //     })
  //   })
  // },
  // delVisitedView({ commit, state }, view) {
  //   return new Promise(resolve => {
  //     commit('DEL_VISITED_VIEW', view)
  //     resolve([...state.visitedViews])
  //   })
  // },
  // delCachedView({ commit, state }, view) {
  //   return new Promise(resolve => {
  //     commit('DEL_CACHED_VIEW', view)
  //     resolve([...state.cachedViews])
  //   })
  // },
  //
  // delOthersViews({ dispatch, state }, view) {
  //   return new Promise(resolve => {
  //     dispatch('delOthersVisitedViews', view)
  //     dispatch('delOthersCachedViews', view)
  //     resolve({
  //       visitedViews: [...state.visitedViews],
  //       cachedViews: [...state.cachedViews],
  //     })
  //   })
  // },
  // delOthersVisitedViews({ commit, state }, view) {
  //   return new Promise(resolve => {
  //     commit('DEL_OTHERS_VISITED_VIEWS', view)
  //     resolve([...state.visitedViews])
  //   })
  // },
  // delOthersCachedViews({ commit, state }, view) {
  //   return new Promise(resolve => {
  //     commit('DEL_OTHERS_CACHED_VIEWS', view)
  //     resolve([...state.cachedViews])
  //   })
  // },
  //
  // delAllViews({ dispatch, state }, view) {
  //   return new Promise(resolve => {
  //     dispatch('delAllVisitedViews', view)
  //     dispatch('delAllCachedViews', view)
  //     resolve({
  //       visitedViews: [...state.visitedViews],
  //       cachedViews: [...state.cachedViews],
  //     })
  //   })
  // },
  // delAllVisitedViews({ commit, state }) {
  //   return new Promise(resolve => {
  //     commit('DEL_ALL_VISITED_VIEWS')
  //     resolve([...state.visitedViews])
  //   })
  // },
  // delAllCachedViews({ commit, state }) {
  //   return new Promise(resolve => {
  //     commit('DEL_ALL_CACHED_VIEWS')
  //     resolve([...state.cachedViews])
  //   })
  // },
  //
  // updateVisitedView({ commit }, view) {
  //   commit('UPDATE_VISITED_VIEW', view)
  // },
}

export default actions
