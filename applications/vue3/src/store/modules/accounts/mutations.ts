import api from '@/api'
import { AccountsState, User } from './state'
import Cookies from 'js-cookie'
import {
  DESTROY_ACCESS_TOKEN,
  DESTROY_CURRENT_USER,
  DESTROY_LOCKED_USER,
  SET_ACCESS_TOKEN,
  SET_USER_INFO,
  SET_LOCKED_USER_INFO,
} from '@/store/modules/accounts/mutations-types'

const mutations = {
  [SET_ACCESS_TOKEN](state: any, accessToken: string) {
    if (accessToken) {
      state.accessToken = accessToken
      api.defaults.headers.common.Authorization = `Bearer ${accessToken}`
      Cookies.set('accessToken', accessToken, { expires: 14 })
    }
  },

  [SET_USER_INFO](state: any, userInfo: User | null) {
    if (userInfo) state.userInfo = userInfo
  },

  [SET_LOCKED_USER_INFO]: (state: AccountsState, userInfo: User) => {
    const { id, email, username } = userInfo
    state.lockedUser = { id, email, username }
  },

  [DESTROY_ACCESS_TOKEN](state: any) {
    state.accessToken = ''
    delete api.defaults.headers.common.Authorization
    Cookies.remove('accessToken')
  },

  [DESTROY_CURRENT_USER](state: any) {
    state.userInfo = null
  },

  [DESTROY_LOCKED_USER]: (state: AccountsState) => {
    state.lockedUser = null
  },
}

export default mutations
