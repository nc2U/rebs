import axios from 'axios'

const api = axios.create({
  baseURL: '/api/',
})

api.defaults.xsrfCookieName = 'csrftoken'
api.defaults.xsrfHeaderName = 'X-CSRFToken'

export default api
