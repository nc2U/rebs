import store from '@/store'
import { hashCode } from '@/utils/helper'
import { RouteRecordRaw } from 'vue-router'

/* Layout Containers */
import DefaultLayout from '@/layouts/DefaultLayout.vue'

/* Router Modules */
import contracts from '@/router/modules/contracts'
import payments from '@/router/modules/payments'
import notices from '@/router/modules/notices'
import projectCash from '@/router/modules/projectCash'
import projectDocs from '@/router/modules/projectDocs'
import projects from '@/router/modules/projects'
import cashes from '@/router/modules/cashes'
import docs from '@/router/modules/docs'
import hrManage from '@/router/modules/hrManage'
import settings from '@/router/modules/settings'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: DefaultLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: '메인 페이지',
        // route level code-splitting
        // this generates a separate chunk (dashboard.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
          import(
            /* webpackChunkName: "dashboard" */ '@/views/_Dashboard/index.vue'
          ),
      },
      {
        path: 'schedule',
        name: '일정 관리',
        component: () =>
          import(/* webpackChunkName: "schedule" */ '@/views/Schedules.vue'),
      },
      contracts,
      payments,
      notices,
      projectCash,
      projectDocs,
      projects,
      cashes,
      docs,
      hrManage,
      settings,
    ],
    beforeEnter: (to, from, next) => {
      const isAuth = store.getters['accounts/isAuthorized']
      if (!isAuth) {
        next({
          name: 'Login',
          query: { redirect: to.fullPath },
        })
      } else {
        next()
      }
    },
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: () => import('@/views/accounts/Login.vue'),
  },
  {
    path: '/accounts/register',
    name: 'Register',
    component: () => import('@/views/accounts/Register.vue'),
    beforeEnter: (to, from, next) => {
      if (
        from.name === 'RegisterCode' &&
        to.query.id == hashCode(store.state.registerCode).toString()
      ) {
        next()
      } else {
        next({
          name: 'RegisterCode',
        })
      }
    },
  },
  {
    path: '/accounts/register-code',
    name: 'RegisterCode',
    component: () => import('@/views/accounts/RegisterCode.vue'),
  },
  {
    path: '/accounts/lock-screen',
    name: 'LockScreen',
    component: () => import('@/views/accounts/LockScreen.vue'),
    beforeEnter: (to, from, next) => {
      const isAuthorized = store.getters['accounts/isAuthorized']
      if (!isAuthorized) {
        next({ name: 'Login' })
      } else {
        next()
      }
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    redirect: '/',
  },
]

export default routes
