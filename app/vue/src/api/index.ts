import axios from 'axios'
import { start, close } from '@/utils/nprogress'
import router from '@/router'

const api = axios.create({
  baseURL: '/api/v1/',
})

api.interceptors.request.use(
  config => {
    start()
    return config
  },
  err => Promise.reject(err),
)

api.interceptors.response.use(
  res => {
    close()
    return res
  },
  err => {
    if (err.response.status == 401)
      return router
        .replace({
          name: 'Login',
          query: { redirect: router.currentRoute.value.fullPath },
        })
        .then(() => close())
    return Promise.reject(err).then(() => close())
  },
)

api.defaults.xsrfCookieName = 'csrftoken'
api.defaults.xsrfHeaderName = 'X-CSRFToken'

export default api
