import store from '@/store'
import { h, resolveComponent } from 'vue'

const projectCash = {
  path: 'project-cash',
  name: '현장자금 관리',
  redirect: '/project-cash/status',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'status',
      name: '현장자금 현황',
      component: () =>
        store.state.accounts.userInfo.staffauth.payment > '0'
          ? import('@/views/projectCash/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'index',
      name: '현장입출 내역',
      component: () =>
        store.state.accounts.userInfo.staffauth.project_cash > '0'
          ? import('@/views/projectCash/List/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'register',
      name: '현장입출 등록',
      component: () =>
        store.state.accounts.userInfo.staffauth.project_cash > '0'
          ? import('@/views/projectCash/Register/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
  ],
}

export default projectCash
