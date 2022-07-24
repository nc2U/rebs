import { DocumentState } from '@/store/modules/document/state'

const mutations = {
  updateState: (state: DocumentState, payload: any) => {
    Object.keys(payload).forEach(key => {
      state[key] = payload[key]
    })
  },
}

export default mutations
