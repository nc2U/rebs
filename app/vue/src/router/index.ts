import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
