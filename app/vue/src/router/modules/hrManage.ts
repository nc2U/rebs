import store from '@/store'
import { h, resolveComponent } from 'vue'

const hrManage = {
  path: 'hr-manage',
  name: '본사인사 관리',
  redirect: '/hr-manage/employee',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'employee',
      name: '직원정보 관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.human_resource > '0'
          ? import('@/views/hrManage/Employee/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '직원정보 관리' },
    },
    {
      path: 'department',
      name: '부서정보 관리',
      component: () =>
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.human_resource > '0'
          ? import('@/views/hrManage/Department/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '부서정보 관리' },
    },
    // {
    //   path: 'rank',
    //   name: '직급정보 관리'
    // }
  ],
}

export default hrManage
