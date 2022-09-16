import { createRouter, createWebHistory } from 'vue-router'
import { start, close } from '@/utils/nprogress'
import routes from '@/router/routes'
import store from '@/store'

const router = createRouter({
  history: createWebHistory(),
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
