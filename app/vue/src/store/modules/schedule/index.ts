import state from './state'
import mutations from './mutations'
import actions from '@/store/modules/schedule/actions'

export default {
  namespaced: true,

  state: () => state,
  mutations,
  actions,
}
