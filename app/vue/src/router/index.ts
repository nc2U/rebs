import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { createRouter, createWebHashHistory } from 'vue-router'
import routes from '@/router/routes'

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(r => !r.meta.auth)) {
    const isAuth = computed(() => useAccount().isAuthorized)
    if (!isAuth.value) next({ name: 'Login', query: { redirect: to.fullPath } })
    else next()
  } else next()
})

export default router
