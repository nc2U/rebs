import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { createRouter, createWebHashHistory } from 'vue-router'
import { start, close } from '@/utils/nprogress'
import routes from '@/router/routes'
// import store from '@/store'

const isAuth = computed(() => useAccount().isAuthorized)

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  // store.commit('startSpinner')
  const auth = await isAuth.value
  if (to.matched.some(r => r.meta.auth))
    if (!auth) next({ name: 'Login', query: { redirect: to.fullPath } })
    else {
      next()
      start()
    }
  else next()
})

router.afterEach(() => {
  // store.commit('endSpinner')
  close()
})

export default router
