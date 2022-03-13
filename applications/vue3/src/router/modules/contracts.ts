import store from '@/store'
import { h, resolveComponent } from 'vue'

const contract = {
  path: 'contracts',
  name: '분양계약 관리',
  redirect: '/contracts/index',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'index',
      name: '계약내역 조회',
      component: () =>
        store.state.accounts.userInfo.staffauth.contract > '0'
          ? import('@/views/contracts/List/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'register',
      name: '계약등록 관리',
      component: () =>
        store.state.accounts.userInfo.staffauth.contract > '0'
          ? import('@/views/contracts/Register/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'cancel',
      name: '계약해지 관리',
      component: () =>
        store.state.accounts.userInfo.staffauth.contract > '0'
          ? import('@/views/contracts/Cancel/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'status',
      name: '동호수 현황표',
      component: () =>
        store.state.accounts.userInfo.staffauth.contract > '0'
          ? import('@/views/contracts/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
  ],
}

export default contract
