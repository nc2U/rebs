import store from '@/store'
import { hashCode } from '@/utils/helper'
import { RouteRecordRaw } from 'vue-router'

/* Layout Containers */
import DefaultLayout from '@/layouts/DefaultLayout.vue'

/* Router Modules */
import contracts from '@/router/modules/contracts'
import payments from '@/router/modules/payments'
import notices from '@/router/modules/notices'
import proCash from '@/router/modules/proCash'
import proDocs from '@/router/modules/proDocs'
import projects from '@/router/modules/projects'
import comCash from '@/router/modules/comCash'
import comDocs from '@/router/modules/comDocs'
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
          import(
            /* webpackChunkName: "schedule" */ '@/views/_Schedules/index.vue'
          ),
      },
      contracts,
      payments,
      notices,
      proCash,
      proDocs,
      projects,
      comCash,
      comDocs,
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
    component: () => import('@/views/_Accounts/Login.vue'),
  },
  {
    path: '/accounts/register',
    name: 'Register',
    component: () => import('@/views/_Accounts/Register.vue'),
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
    component: () => import('@/views/_Accounts/RegisterCode.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/',
  },
]

export default routes
