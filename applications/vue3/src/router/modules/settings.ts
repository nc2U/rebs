import store from '@/store'
import { h, resolveComponent } from 'vue'

const settings = {
  path: 'settings',
  name: '환경설정',
  redirect: '/settings/company',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'company',
      name: '회사정보 관리',
      component: () =>
        store.state.accounts.userInfo.staffauth.company_settings > '0'
          ? import('@/views/settings/Company/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'authorization',
      name: '권한설정 관리',
      component: () =>
        store.state.accounts.userInfo.staffauth.auth_manage > '0'
          ? import('@/views/settings/Authorization/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'users',
      name: '사용자 관리',
      component: () => import('@/views/settings/Users/Index.vue'),
    },
  ],
}

export default settings
