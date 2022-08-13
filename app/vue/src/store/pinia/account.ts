import api from '@/api'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { Buffer } from 'buffer'
import Cookies from 'js-cookie'
import { errorHandle, message } from '@/utils/helper'
import { StaffAuth } from '@/store/modules/accounts/state'

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

export const useAccount = defineStore('account', () => {
  // states
  const accessToken = ref('')
  const userInfo = ref<User | null>(null)
  const lockedUser = ref<LockedUser | null>(null)
  const todoList = ref<Todo[]>([])

  // getters
  const superAuth = computed(() => userInfo.value?.is_superuser)
  const staffAuth = computed(() =>
    userInfo.value?.staffauth ? userInfo.value.staffauth : null,
  )
  const isAuthorized = computed(
    () => accessToken.value.length && !!userInfo.value,
  )
  const initComId = computed(() =>
    userInfo.value?.staffauth?.company ? userInfo.value.staffauth.company : 1,
  )
  const initProjId = computed(() =>
    userInfo.value?.staffauth?.assigned_project
      ? userInfo.value.staffauth.assigned_project
      : userInfo.value?.staffauth?.allowed_projects[0] || 1,
  )
  const myTodos = computed(() =>
    todoList.value.filter(
      todo => !todo.soft_deleted && todo.user === userInfo.value?.pk,
    ),
  )

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

  const login = (payload: {
    email: string
    password: string
    redirect?: string
  }) => {
    const { redirect, ...loginData } = payload
    return api
      .post('/token/', loginData)
      .then(res => {
        setToken(res.data.access)
        return api.get(`/user/${extractId(accessToken.value)}`)
      })
      .then(res => {
        setUser(res.data)
        message('', '', '로그인 성공 알림!')
      })
      .catch(err => console.log(err))
  }

  const loginByToken = (token?: string) => {
    if (token) {
      setToken(token)
      return api
        .get(`/user/${extractId(token)}`)
        .then(res => setUser(res.data))
        .catch(err => {
          console.log(err.response.data)
        })
    } else return Promise.resolve()
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
        todoList.value = res.data.results
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createTodo = (payload: { user: number; title: string }) => {
    api
      .post('/todo/', payload)
      .then(() => {
        fetchTodoList()
        return api
          .get(`/user/${userInfo.value?.pk}/`)
          .then(res => {
            userInfo.value = res.data
          })
          .catch(err => errorHandle(err.response.data))
      })
      .catch(err => errorHandle(err.response.data))
  }

  const patchTodo = (payload: any) => {
    const { pk } = payload
    delete payload.pk
    api
      .patch(`/todo/${pk}/`, payload)
      .then(() => {
        fetchTodoList()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteTodo = (pk: string) => {
    api
      .delete(`/todo/${pk}/`)
      .then(() => {
        fetchTodoList()
        return api
          .get(`/user/${userInfo.value?.pk}/`)
          .then(res => {
            userInfo.value = res.data
          })
          .catch(err => errorHandle(err.response.data))
      })
      .catch(err => errorHandle(err.response.data))
  }

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
    createTodo,
    patchTodo,
    deleteTodo,
  }
})
