import axios from 'axios'
import router from '@/router'
import { start, close } from '@/utils/nprogress'

const api = axios.create({
  baseURL: '/api/v1/',
})

api.interceptors.request.use(
  config => {
    start()
    return config
  },
  error => Promise.reject(error),
)

api.interceptors.response.use(
  response => {
    close()
    return response
  },
  error => {
    if (error.response.status == 401)
      return router
        .replace({
          name: 'Login',
          query: { redirect: router.currentRoute.value.fullPath },
        })
        .then(() => close())
    return Promise.reject(error).then(() => close())
  },
)

api.defaults.xsrfCookieName = 'csrftoken'
api.defaults.xsrfHeaderName = 'X-CSRFToken'

export default api
