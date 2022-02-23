import state from './state'
import getters from './getters'
import mutations from './mutations'
import actions from './actions'

const pCash = {
  namespaced: true,

  state: () => state,
  getters,
  mutations,
  actions,
}

export default pCash
