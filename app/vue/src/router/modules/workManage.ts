import { h, resolveComponent } from 'vue'

const workManage = {
  path: 'work',
  name: '업 무 관 리',
  redirect: '/work/mytask',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    // {
    //   path: 'mytask',
    //   name: '내 페이지',
    //   component: () => import('@/views/_WorkManage/MyTask/Index.vue'),
    //   meta: { title: '내 페이지', auth: true },
    // },
    {
      path: 'projects',
      name: '프로젝트',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'admin',
      name: '관리 메뉴',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
  ],
}

export default workManage
