import store from '@/store'
import { h, resolveComponent } from 'vue'

const comCash = {
  path: 'cashes',
  name: '본사회계 관리',
  redirect: '/cashes/status',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'status',
      name: '본사자금 현황',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.company_cash > '0'
          ? import('@/views/comCash/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'index',
      name: '본사출납 관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.company_cash > '0'
          ? import('@/views/comCash/Manage/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
  ],
}

export default comCash
