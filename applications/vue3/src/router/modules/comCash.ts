import store from '@/store'
import {h, resolveComponent} from 'vue'

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
        store.state.accounts.userInfo.staffauth.company_cash > '0'
          ? import('@/views/comCash/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'index',
      name: '본사입출 내역',
      component: () =>
        store.state.accounts.userInfo.staffauth.company_cash > '0'
          ? import('@/views/comCash/Manage/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'register',
      name: '본사입출 등록',
      component: () =>
        store.state.accounts.userInfo.staffauth.company_cash > '0'
          ? import('@/views/comCash/Register/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
  ],
}

export default comCash
