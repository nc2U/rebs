import api from '@/api'
import Cookies from 'js-cookie'
import { Buffer } from 'buffer'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import type { User, StaffAuth, Profile, Scrape, Todo } from '@/store/types/accounts'
import { useDocument } from '@/store/pinia/document'
import type { LocationQueryValue } from 'vue-router'

type LoginUser = { email: string; password: string }

const extractId = (token: string) => {
  const base64Payload = token.split('.')[1]
  const payload = Buffer.from(base64Payload, 'base64')
  const result = JSON.parse(payload.toString())
  return result.user_id ? result.user_id : null
}

export const useAccount = defineStore('account', () => {
  // states
  const user = ref<User | null>(null)
  const userInfo = ref<User | null>(null)
  const usersList = ref<User[]>([])
  const accessToken = ref<string>('')
  const passChecked = ref(false)

  // getters
  const getUsers = computed(() =>
    usersList.value.map((u: User) => ({ value: u.pk as number, label: u.username })),
  )
  const isAuthorized = computed(() => !!accessToken.value && !!userInfo.value)

  // actions
  const fetchUsersList = () =>
    api
      .get('/user/?is_active=true')
      .then(res => (usersList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchUser = (pk: number) =>
    api
      .get(`/user/${pk}/`)
      .then(res => (user.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const signup = (payload: LoginUser & { username: string }) =>
    api
      .post('/user/', payload)
      .then(() => message('info', '', '회원가입이 완료되었습니다.'))
      .catch(err => errorHandle(err.response.data))

  const setToken = (token: string) => {
    accessToken.value = token
    api.defaults.headers.common.Authorization = `Bearer ${accessToken.value}`
    Cookies.set('accessToken', accessToken.value, { expires: 14 })
  }

  const setUser = (user: User) => {
    userInfo.value = user
    fetchTodoList().then(() => fetchProfile())
  }

  const login = async (payload: LoginUser) => {
    Cookies.remove('accessToken')
    return await api
      .post('/token/', payload)
      .then(res => {
        setToken(res.data.access)
        return api.get(`/user/${extractId(accessToken.value)}/`)
      })
      .then(res => {
        if (!!res.data.profile) setUser(res.data)
        return res.data
      })
      .catch(() => message('warning', '', '이메일 또는 비밀번호를 확인하여 주세요.'))
  }

  const loginByToken = async (token?: string) => {
    if (token) {
      setToken(token)
      return await api
        .get(`/user/${extractId(token)}/`)
        .then(res => setUser(res.data))
        .catch(() => {
          userInfo.value = null
          profile.value = null
          todoList.value = []
          accessToken.value = ''
          delete api.defaults.headers.common.Authorization
          Cookies.remove('accessToken')
        })
    } else return Promise.resolve()
  }

  const logout = () => {
    userInfo.value = null
    profile.value = null
    todoList.value = []
    accessToken.value = ''
    delete api.defaults.headers.common.Authorization
    Cookies.remove('accessToken')
    message('info', '', '로그아웃 완료 알림!')
  }

  const checkPassword = (payload: LoginUser) =>
    api
      .post(`/check-password/`, payload)
      .then(() => (passChecked.value = true))
      .catch(() => message('warning', '', '비밀번호를 확인하여 주세요.'))

  const changePassword = (payload: { old_password: string; new_password: string }) =>
    api
      .post(`/change-password/`, payload)
      .then(res => {
        message('success', '', res.data.detail)
        return res.data
      })
      .catch(err => errorHandle(err.response.data))

  const passReset = (payload: { email: string }) =>
    api
      .post('password-reset/', payload)
      .then(res => message(undefined, '', '비밀번호 초기화 안내메일을 발송했습니다.'))
      .catch(err => errorHandle(err.response.data))

  const passResetConfirm = (payload: {
    user_id: LocationQueryValue | LocationQueryValue[]
    token: LocationQueryValue | LocationQueryValue[]
    new_password: string
  }) => {
    const { user_id, token, new_password } = payload
    api
      .post(`/password-reset-confirm/${user_id}/${token}/`, { new_password })
      .then(res => message('success', '', '비밀번호를 성공적으로 재설정하였습니다.'))
      .catch(err => errorHandle(err.response.data))
  }

  const resetTokenList = ref<
    {
      pk: number
      user: number
      token: string
      updated: string
      is_expired: boolean
    }[]
  >([])
  const fetchResetTokenList = (user: number) =>
    api
      .get(`/pass-reset-token/?user=${user}`)
      .then(res => (resetTokenList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  // const fetchResetToken = (pk: number) =>
  //   api
  //     .get(`/pass-reset-token/${pk}/`)
  //     .then(res => (resetToken.value = res.data))
  //     .catch(err => errorHandle(err.response.data))

  // getters
  const superAuth = computed(() => userInfo.value?.is_superuser)
  const workManager = computed(() => userInfo.value?.work_manager || superAuth.value)
  const staffAuth = computed(() => (userInfo.value?.staffauth ? userInfo.value.staffauth : null))
  const isStaff = computed(() => staffAuth.value?.is_staff || superAuth.value)

  const writeComDocs = computed(() => superAuth.value || staffAuth.value?.company_docs == '2')
  const writeProDocs = computed(
    () => superAuth.value || writeComDocs.value || staffAuth.value?.project_docs == '2',
  )
  const isComCash = computed(() => superAuth.value || Number(staffAuth.value?.company_cash || null))
  const writeComCash = computed(() => superAuth.value || staffAuth.value?.company_cash == '2')
  const writeProCash = computed(
    () => superAuth.value || writeComCash.value || staffAuth.value?.project_cash == '2',
  )

  // actions
  const createAuth = async (payload: StaffAuth, userPk: number) => {
    payload.user = userPk
    return await api
      .post(`/staff-auth/`, payload)
      .then(() => api.get(`/user/${userPk}/`).then(() => fetchUser(userPk).then(() => message())))
      .catch(err => errorHandle(err.response.data))
  }

  const patchAuth = async (payload: StaffAuth, userPk: number) => {
    const { pk, ...authData } = payload
    return await api
      .patch(`/staff-auth/${pk}/`, authData)
      .then(() => api.get(`/user/${userPk}/`).then(() => fetchUser(userPk).then(() => message())))
      .catch(err => errorHandle(err.response.data))
  }

  // states
  const profile = ref<Profile | null>(null)

  // actions
  const fetchProfile = async () => {
    const profilePk = userInfo.value?.profile?.pk ?? null
    return profilePk
      ? await api
          .get(`/profile/${profilePk}/`)
          .then(res => (profile.value = res.data))
          .catch(err => errorHandle(err.response.data))
      : null
  }

  const createProfile = async (payload: FormData) => {
    api.defaults.headers.post['Content-Type'] = 'multipart/form-data'
    return await api
      .post(`/profile/`, payload)
      .then(() => {
        const cookedToken = Cookies.get('accessToken')
        loginByToken(cookedToken).then(() => message())
      })
      .catch(err => errorHandle(err.response.data))
  }

  const patchProfile = async (payload: { pk: number; form: FormData }) => {
    const { pk, form } = payload
    api.defaults.headers.patch['Content-Type'] = 'multipart/form-data'
    return await api
      .patch(`/profile/${pk}/`, form)
      .then(() => {
        const cookedToken = Cookies.get('accessToken')
        loginByToken(cookedToken).then(() => message())
      })
      .catch(err => errorHandle(err.response.data))
  }

  // states
  const scrape = ref<Scrape | null>(null)
  const scrapeList = ref<Scrape[]>([])
  const scrapeCount = ref(0)

  // actions
  const scrapePages = (itemsPerPage: number) => Math.ceil(scrapeCount.value / itemsPerPage)
  const fetchScrape = (pk: number) =>
    api
      .get(`/scrape/${pk}/`)
      .then(res => (scrape.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchScrapeList = (page = 1) =>
    api
      .get(`/scrape/?user=${userInfo.value?.pk ?? ''}&page=${page}`)
      .then(res => {
        scrapeList.value = res.data.results
        scrapeCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))

  const docStore = useDocument()

  const createScrape = (payload: { post: number; user: number }) =>
    api
      .post('/scrape/', payload)
      .then(() => docStore.fetchPost(payload.post))
      .catch(err => errorHandle(err.response.data))

  const patchScrape = (pk: number, title: string) =>
    api
      .patch(`/scrape/${pk}/`, { title })
      .then(() => fetchScrapeList().then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteScrape = (pk: number) =>
    api
      .delete(`/scrape/${pk}/`)
      .then(() =>
        fetchScrapeList().then(() =>
          message('warning', '', '해당 포스트 스크랩을 취소하였습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // states
  const todoList = ref<Todo[]>([])

  // getters
  const myTodos = computed(() =>
    todoList.value.filter(todo => !todo.soft_deleted && todo.user === userInfo.value?.pk),
  )

  const fetchTodoList = async () => {
    const url = userInfo.value ? `/todo/?user=${userInfo.value.pk}&soft_deleted=false` : '/todo/'
    return await api
      .get(url)
      .then(res => {
        todoList.value = res.data.results
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createTodo = (payload: Todo) =>
    api
      .post('/todo/', payload)
      .then(() => {
        fetchTodoList().then(() =>
          api
            .get(`/user/${userInfo.value?.pk}/`)
            .then(res => {
              userInfo.value = res.data
            })
            .catch(err => errorHandle(err.response.data)),
        )
      })
      .catch(err => errorHandle(err.response.data))

  const patchTodo = (payload: Todo) =>
    api
      .patch(`/todo/${payload.pk}/`, payload)
      .then(() => fetchTodoList())
      .catch(err => errorHandle(err.response.data))

  const deleteTodo = (pk: number) =>
    api
      .delete(`/todo/${pk}/`)
      .then(() => {
        fetchTodoList().then(() =>
          api
            .get(`/user/${userInfo.value?.pk}/`)
            .then(res => {
              userInfo.value = res.data
            })
            .catch(err => errorHandle(err.response.data)),
        )
      })
      .catch(err => errorHandle(err.response.data))

  return {
    user,
    userInfo,
    usersList,
    accessToken,
    passChecked,

    getUsers,
    isAuthorized,

    fetchUsersList,
    fetchUser,
    signup,
    login,
    loginByToken,
    logout,
    checkPassword,
    changePassword,
    passReset,
    passResetConfirm,

    resetTokenList,
    fetchResetTokenList,

    superAuth,
    workManager,
    staffAuth,
    isStaff,
    writeComDocs,
    writeProDocs,
    isComCash,
    writeComCash,
    writeProCash,

    createAuth,
    patchAuth,

    profile,

    fetchProfile,
    createProfile,
    patchProfile,

    scrape,
    scrapeList,
    scrapeCount,

    scrapePages,
    fetchScrape,
    fetchScrapeList,
    createScrape,
    patchScrape,
    deleteScrape,

    todoList,
    myTodos,

    fetchTodoList,
    createTodo,
    patchTodo,
    deleteTodo,
  }
})
