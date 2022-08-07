import state from './state'
import getters from '@/store/modules/schedule/getters'
import mutations from './mutations'
import actions from '@/store/modules/schedule/actions'

export default {
  namespaced: true,

  state: () => state,
  getters,
  mutations,
  actions,
}
