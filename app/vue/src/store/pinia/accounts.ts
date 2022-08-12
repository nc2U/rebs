import api from '@/api'
import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import { State } from '@/store'
import { Buffer } from 'buffer'
import router from '@/router'
import Cookies from 'js-cookie'
import { errorHandle, message } from '@/utils/helper'

export declare interface StaffAuth {
  pk: number
  company: number
  is_staff: boolean
  assigned_project: number
  allowed_projects: number[]
  contract: string
  payment: string
  notice: string
  project_cash: string
  project_docs: string
  human_resource: string
  company_settings: string
  auth_manage: string
}

interface Profile {
  pk: number
  user: number
  name: string
  birth_date: string
  cell_phone: string
  image: string | null
}

export declare interface Todo {
  pk: number
  url: string
  user: number
  title: string
  completed: boolean
  soft_deleted: boolean
}

export declare interface User {
  pk: number
  email: string
  username: string
  is_active: boolean
  date_joined: string
  is_superuser: boolean
  staffauth: StaffAuth | null
  profile: Profile | null
  todos: Todo[]
}

export declare interface LockedUser {
  pk: number
  email: string
  username: string
}

export declare interface AccountsState extends State {
  accessToken: string
  userInfo: User | null
  lockedUser: LockedUser | null
  todoList: Todo[]
}

export const useAccount = defineStore('account', () => {
  // states
  const accessToken = ref('')
  const userInfo = ref<User | null>(null)
  const lockedUser = ref<LockedUser | null>(null)
  const todoList = ref<Todo[]>([])

  // getters
  const superAuth = () => userInfo.value?.is_superuser
  const staffAuth = () =>
    userInfo.value?.staffauth ? userInfo.value.staffauth : null
  const isAuthorized = () => accessToken.value.length && !!userInfo.value
  const initComId = () =>
    userInfo.value?.staffauth?.company ? userInfo.value.staffauth.company : 1
  const initProjId = () =>
    userInfo.value?.staffauth?.assigned_project
      ? userInfo.value.staffauth.assigned_project
      : userInfo.value?.staffauth?.allowed_projects[0] || 1
  const myTodos = () =>
    userInfo.value
      ? todoList.value.filter(
          todo => !todo.soft_deleted && todo.user === userInfo.value?.pk,
        )
      : []

  // actions
  const extractId = (token: string) => {
    const base64Payload = token.split('.')[1]
    const payload = Buffer.from(base64Payload, 'base64')
    const result = JSON.parse(payload.toString())
    return result.user_id ? result.user_id : null
  }

  const signup = (payload: {
    email: string
    username: string
    password: string
  }) => {
    api
      .post('/user/', payload)
      .then(() => {
        router.push({ name: 'Login' })
        message('info', '', '회원가입이 완료되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  const setToken = (token: string) => {
    accessToken.value = token
    api.defaults.headers.common.Authorization = `Bearer ${accessToken.value}`
    Cookies.set('accessToken', accessToken.value, { expires: 14 })
  }

  const setUser = (user: User) => {
    userInfo.value = user
    lockedUser.value = user
    fetchTodoList()
  }

  const login = (payload: { email: string; password: string }) => {
    return api
      .post('/token/', payload)
      .then(res => {
        setToken(res.data.access)
        return api.get(`/user/${extractId(accessToken.value)}`)
      })
      .then(res => {
        setUser(res.data)
        message('', '', '로그인 성공 알림!')
      })
      .catch(err => console.log(err.response.data))
  }

  const loginByToken = (token?: string) => {
    if (token) {
      setToken(token)
      return api
        .get(`/user/${extractId(token)}`)
        .then(res => setUser(res.data))
        .catch(err => {
          router.push({ name: 'Login' })
          console.log(err.response.data)
        })
    } else router.push({ name: 'Login' })
  }

  const logout = () => {
    userInfo.value = null
    lockedUser.value = null
    todoList.value = []
    accessToken.value = ''
    delete api.defaults.headers.common.Authorization
    Cookies.remove('accessToken')
    message('', '', '로그아웃 완료 알림!')
  }

  const createProfile = (form: Profile) => {
    api.defaults.headers.post['Content-Type'] = 'multipart/form-data'
    api
      .post(`/profile/`, form)
      .then(() => {
        const cookedToken = Cookies.get('accessToken')
        loginByToken(cookedToken)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const patchProfile = (payload: { pk: string; form: Profile }) => {
    const { pk, form } = payload
    api.defaults.headers.patch['Content-Type'] = 'multipart/form-data'
    api
      .patch(`/profile/${pk}/`, form)
      .then(() => {
        const cookedToken = Cookies.get('accessToken')
        loginByToken(cookedToken)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const fetchTodoList = () => {
    const url = userInfo.value
      ? `/todo/?user=${userInfo.value.pk}&soft_deleted=false`
      : '/todo/'
    api
      .get(url)
      .then(res => {
        todoList.value = res.data
      })
      .catch(err => errorHandle(err.response.data))
  }

  // createTodo: (
  //   { commit, dispatch, state }: any,
  //   payload: { user: number; title: string },
  // ) => {
  //   api
  //     .post('/todo/', payload)
  //     .then(() => {
  //       dispatch('fetchTodoList')
  //       return api
  //         .get(`/user/${state.userInfo.pk}/`)
  //         .then(res => {
  //           commit(SET_USER_INFO, res.data)
  //         })
  //         .catch(err => errorHandle(err.response.data))
  //     })
  //     .catch(err => errorHandle(err.response.data))
  // },
  //
  // patchTodo: ({ dispatch }: any, payload: any) => {
  //   const { pk } = payload
  //   delete payload.pk
  //   api
  //     .patch(`/todo/${pk}/`, payload)
  //     .then(() => {
  //       dispatch('fetchTodoList')
  //     })
  //     .catch(err => errorHandle(err.response.data))
  // },
  //
  // deleteTodo: ({ commit, dispatch, state }: any, pk: any) => {
  //   api
  //     .delete(`/todo/${pk}/`)
  //     .then(() => {
  //       dispatch('fetchTodoList')
  //       return api
  //         .get(`/user/${state.userInfo.pk}/`)
  //         .then(res => {
  //           commit(SET_USER_INFO, res.data)
  //         })
  //         .catch(err => errorHandle(err.response.data))
  //     })
  //     .catch(err => errorHandle(err.response.data))
  // },

  return {
    accessToken,
    userInfo,
    lockedUser,
    todoList,

    superAuth,
    staffAuth,
    isAuthorized,
    initComId,
    initProjId,
    myTodos,

    signup,
    login,
    loginByToken,
    logout,

    createProfile,
    patchProfile,

    fetchTodoList,
  }
})
