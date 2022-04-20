import api from '@/api'
import {
  DESTROY_ACCESS_TOKEN,
  DESTROY_CURRENT_USER,
  FETCH_TODO_LIST,
  SET_ACCESS_TOKEN,
  SET_LOCKED_USER,
  SET_USER_INFO,
} from '@/store/modules/accounts/mutations-types'
import router from '@/router'
import { message } from '@/utils/helper'
import Cookies from 'js-cookie'

declare const Buffer: any

const extractId = (token: string) => {
  const base64Payload = token.split('.')[1]
  const payload = Buffer.from(base64Payload, 'base64')
  const result = JSON.parse(payload.toString())
  return result.user_id ? result.user_id : null
}

const actions = {
  signup(
    store: any,
    payload: { email: string; username: string; password: string },
  ) {
    api
      .post(`/user/`, payload)
      .then(() => {
        router.push({ name: 'Login' })
        message('info', '', '회원가입이 완료되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },
  login(
    { commit, dispatch }: any,
    payload: { email: string; password: string },
  ) {
    const { email, password } = payload
    return api
      .post('/token/', { email, password })
      .then(res => {
        const token = res.data.access
        commit(SET_ACCESS_TOKEN, token)
        const pk = extractId(token)
        return api.get(`/user/${pk}/`)
      })
      .then(res => {
        commit(SET_USER_INFO, res.data)
        commit(SET_LOCKED_USER, res.data)
        dispatch('fetchTodoList')
        message('', '', '로그인 성공 알림!')
      })
      .catch(err => {
        console.log(err.response.data)
        alert('이메일 또는 비밀번호를 확인하세요.')
      })
  },

  loginByToken({ commit, dispatch }: any, token?: string) {
    if (token) {
      commit(SET_ACCESS_TOKEN, token)
      const pk = extractId(token)
      return api
        .get(`/user/${pk}/`)
        .then(res => {
          commit(SET_USER_INFO, res.data)
          commit(SET_LOCKED_USER, res.data)
          dispatch('fetchTodoList')
        })
        .catch(err => console.log(err.response.data))
    } else return
  },

  logout({ commit }: any) {
    commit(DESTROY_CURRENT_USER)
    commit(DESTROY_ACCESS_TOKEN)
    message('', '', '로그아웃 완료 알림!')
  },

  logoutNoMessage({ commit }: any) {
    commit(DESTROY_CURRENT_USER)
    commit(DESTROY_ACCESS_TOKEN)
  },

  createProfile: ({ dispatch }: any, payload: any) => {
    api
      .post(`/profile/`, payload)
      .then(() => {
        const cookedToken = Cookies.get('accessToken')
        dispatch('loginByToken', cookedToken)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  patchProfile: ({ dispatch }: any, payload: any) => {
    const { pk, ...profileData } = payload
    api
      .patch(`/profile/${pk}/`, profileData)
      .then(() => {
        const cookedToken = Cookies.get('accessToken')
        dispatch('loginByToken', cookedToken)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  fetchTodoList: (store: any) => {
    const url = store.state.userInfo
      ? `/todo/?user=${store.state.userInfo.pk}&soft_deleted=false`
      : '/todo/'
    api
      .get(url)
      .then(res => {
        store.commit(FETCH_TODO_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createTodo: (
    { commit, dispatch, state }: any,
    payload: { user: number; title: string },
  ) => {
    api
      .post('/todo/', payload)
      .then(() => {
        dispatch('fetchTodoList')
        return api
          .get(`/user/${state.userInfo.pk}/`)
          .then(res => {
            commit(SET_USER_INFO, res.data)
          })
          .catch(err => console.log(err.response.data))
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  patchTodo: ({ dispatch }: any, payload: any) => {
    const { pk } = payload
    delete payload.pk
    api
      .patch(`/todo/${pk}/`, payload)
      .then(() => {
        dispatch('fetchTodoList')
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  deleteTodo: ({ commit, dispatch, state }: any, pk: any) => {
    api
      .delete(`/todo/${pk}/`)
      .then(() => {
        dispatch('fetchTodoList')
        return api
          .get(`/user/${state.userInfo.pk}/`)
          .then(res => {
            commit(SET_USER_INFO, res.data)
          })
          .catch(err => console.log(err.response.data))
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },
}

export default actions
