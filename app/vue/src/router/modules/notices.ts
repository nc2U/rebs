import store from '@/store'
import { h, resolveComponent } from 'vue'

const notices = {
  path: 'notices',
  name: '고객고지 관리',
  redirect: '/notices/bill',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'bill',
      name: '수납고지서 출력',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.notice > '0'
          ? import('@/views/notices/Bill/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '수납고지서 출력' },
    },
    {
      path: 'sms',
      name: 'SMS 발송관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.notice > '0'
          ? import('@/views/notices/Sms/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: 'SMS 발송관리' },
    },
    {
      path: 'mailing',
      name: 'MAIL 발송관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.notice > '0'
          ? import('@/views/notices/Mailing/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: 'MAIL 발송관리' },
    },
    {
      path: 'post-label',
      name: '우편라벨 관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.notice > '0'
          ? import('@/views/notices/Label/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '우편라벨 관리' },
    },
    {
      path: 'log',
      name: '발송기록 관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.notice > '0'
          ? import('@/views/notices/Log/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '발송기록 관리' },
    },
  ],
}

export default notices
