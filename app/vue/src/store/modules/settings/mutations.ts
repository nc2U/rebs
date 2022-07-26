import {
  FETCH_COMPANY,
  FETCH_COMPANY_LIST,
} from '@/store/modules/settings/mutations-types'
import { Company, CompanyState } from '@/store/modules/settings/state'

const mutations = {
  updateState: (state: CompanyState, payload: any) => {
    Object.keys(payload).forEach(key => {
      state[key] = payload[key]
    })
  },

  [FETCH_COMPANY_LIST]: (state: CompanyState, payload: any) => {
    state.companyList = payload.results
  },

  [FETCH_COMPANY]: (state: CompanyState, payload: Company) => {
    state.company = payload
  },
}

export default mutations
