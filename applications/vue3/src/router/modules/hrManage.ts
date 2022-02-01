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
      component: () => import('@/views/hrManage/Employee/Index.vue'),
    },
    {
      path: 'department',
      name: '부서정보 관리',
      component: () => import('@/views/hrManage/Department/Index.vue'),
    },
    // {
    //   path: 'rank',
    //   name: '직급정보 관리'
    // }
  ],
}

export default hrManage
