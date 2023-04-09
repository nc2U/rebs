import { computed } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import { start, close } from '@/utils/nprogress'
import routes from '@/router/routes'
import store from '@/store'
import { useAccount } from '@/store/pinia/account'

const isAuth = computed(() => useAccount().isAuthorized)

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  start()
  store.commit('startSpinner')
  if (!isAuth.value && to.name !== 'Login') {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }
  next()
})

router.afterEach(() => {
  store.commit('endSpinner')
  close()
})

export default router
