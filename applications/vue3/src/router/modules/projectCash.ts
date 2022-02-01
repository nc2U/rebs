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
      component: () => import('@/views/projectCash/Status/Index.vue'),
    },
    {
      path: 'index',
      name: '현장입출 내역',
      component: () => import('@/views/projectCash/List/Index.vue'),
    },
    {
      path: 'register',
      name: '현장입출 등록',
      component: () => import('@/views/projectCash/Register/Index.vue'),
    },
  ],
}

export default projectCash
