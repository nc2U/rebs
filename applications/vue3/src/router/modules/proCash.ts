import store from '@/store'
import {h, resolveComponent} from 'vue'

const proCash = {
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
        store.state.accounts.userInfo.staffauth.project_cash > '0'
          ? import('@/views/proCash/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'index',
      name: '현장출납 기록',
      component: () =>
        store.state.accounts.userInfo.staffauth.project_cash > '0'
          ? import('@/views/proCash/Manage/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
  ],
}

export default proCash
