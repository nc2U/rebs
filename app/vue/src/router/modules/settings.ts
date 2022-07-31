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
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.company_settings > '0'
          ? import('@/views/settings/Company/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '회사정보 관리' },
    },
    {
      path: 'authorization',
      name: '권한설정 관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.auth_manage > '0'
          ? import('@/views/settings/Authorization/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '권한설정 관리' },
    },
    {
      path: 'profile',
      name: '프로필 관리',
      component: () => import('@/views/settings/Profile/Index.vue'),
      meta: { title: '프로필 관리' },
    },
  ],
}

export default settings
