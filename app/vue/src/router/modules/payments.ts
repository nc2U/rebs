import store from '@/store'
import { h, resolveComponent } from 'vue'

const payments = {
  path: 'payments',
  name: '분양수납 관리',
  redirect: '/payments/index',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'index',
      name: '분양수납 내역',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.payment > '0'
          ? import('@/views/payments/List/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '분양수납 내역' },
    },
    {
      path: 'manage',
      name: '건별수납 관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.payment > '0'
          ? import('@/views/payments/Register/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '건별수납 관리' },
    },
  ],
}

export default payments
