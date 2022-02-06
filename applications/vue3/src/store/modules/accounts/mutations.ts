import api from '@/api'
import { AccountsState, Todo, User } from './state'
import Cookies from 'js-cookie'
import {
  DESTROY_ACCESS_TOKEN,
  DESTROY_CURRENT_USER,
  DESTROY_LOCKED_USER,
  FETCH_TODO_LIST,
  SET_ACCESS_TOKEN,
  SET_LOCKED_USER,
  SET_USER_INFO,
} from '@/store/modules/accounts/mutations-types'

const mutations = {
  [SET_ACCESS_TOKEN]: (state: AccountsState, accessToken: string) => {
    if (accessToken) {
      state.accessToken = accessToken
      api.defaults.headers.common.Authorization = `Bearer ${accessToken}`
      Cookies.set('accessToken', accessToken, { expires: 14 })
    }
  },

  [SET_USER_INFO]: (state: AccountsState, userInfo: User | null) => {
    if (userInfo) state.userInfo = userInfo
  },

  [SET_LOCKED_USER]: (state: AccountsState, payload: any) => {
    const { pk, email, username } = payload
    state.lockedUser = { pk, email, username }
  },

  [DESTROY_ACCESS_TOKEN]: (state: AccountsState) => {
    state.accessToken = ''
    delete api.defaults.headers.common.Authorization
    Cookies.remove('accessToken')
  },

  [DESTROY_CURRENT_USER]: (state: AccountsState) => {
    state.userInfo = null
  },

  [DESTROY_LOCKED_USER]: (state: AccountsState) => {
    state.lockedUser = null
  },

  [FETCH_TODO_LIST]: (state: AccountsState, payload: Todo[]) => {
    state.todoList = payload
  },
}

export default mutations
