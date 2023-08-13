import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { createRouter, createWebHashHistory } from 'vue-router'
import routes from '@/router/routes'

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

const isAuth = computed(() => useAccount().isAuthorized)

router.beforeEach((to, from, next) => {
  if (to.matched.some(r => r.meta.auth))
    if (!isAuth.value) next({ name: 'Login', query: { redirect: to.fullPath } })
    else next()
  else next()
})

export default router
