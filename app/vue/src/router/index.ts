import { createRouter, createWebHashHistory } from 'vue-router'
import { start, close } from '@/utils/nprogress'
import routes from '@/router/routes'
import store from '@/store'

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  start()
  store.commit('startSpinner')
  next()
})

router.afterEach(() => {
  store.commit('endSpinner')
  close()
})

export default router
