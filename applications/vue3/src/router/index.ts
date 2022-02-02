import { createRouter, createWebHashHistory } from 'vue-router'
import routes from '@/router/routes'
import store from '@/store'

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  store.commit('startSpinner')
  next()
})

router.afterEach((to, from) => {
  store.commit('endSpinner')
})

export default router
