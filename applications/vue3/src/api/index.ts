import axios from 'axios'
import store from '@/store'

const api = axios.create({
  baseURL: '/api/',
})

api.interceptors.request.use(
  (config) => {
    store.commit('startSpinner')
    return config
  },
  (error) => {
    // alert('데이터 요청 실패!')
    return Promise.reject(error)
  },
)

api.interceptors.response.use(
  (response) => {
    store.commit('endSpinner')
    return response
  },
  (error) => {
    // alert('데이터 응답 실패!')
    return Promise.reject(error)
  },
)

api.defaults.xsrfCookieName = 'csrftoken'
api.defaults.xsrfHeaderName = 'X-CSRFToken'

export default api
