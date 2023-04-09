import store from '@/store'
import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
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

const isAuth = computed(() => useAccount().isAuthorized)

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: DefaultLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: '대 시 보 드',
        // route level code-splitting
        // this generates a separate chunk (dashboard.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
          import(
            /* webpackChunkName: "dashboard" */ '@/views/_Dashboard/index.vue'
          ),
        meta: { title: '대 시 보 드', affix: true },
      },
      {
        path: 'schedule',
        name: '일 정 관 리',
        component: () =>
          import(
            /* webpackChunkName: "schedule" */ '@/views/_Schedules/index.vue'
          ),
        meta: { title: '일 정 관 리', affix: true },
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
      {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/components/NotFound.vue'),
        meta: { title: 'Not-Found', except: true },
        beforeEnter: (to, from, next) => {
          if (!!isAuth.value) {
            next()
          } else {
            next({
              path: '/accounts/login',
              query: { redirect: to.fullPath },
            })
          }
        },
      },
    ],
    beforeEnter: (to, from, next) => {
      if (!!isAuth.value) {
        next()
      } else {
        next({
          path: '/accounts/login',
          query: { redirect: to.fullPath },
        })
      }
    },
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: () => import('@/views/_Accounts/Login.vue'),
    meta: { title: '로그인', except: true },
  },
  {
    path: '/accounts/register',
    name: 'Register',
    component: () => import('@/views/_Accounts/Register.vue'),
    meta: { title: '회원가입', except: true },
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
    meta: { title: '코드입력', except: true },
  },
]

export default routes
