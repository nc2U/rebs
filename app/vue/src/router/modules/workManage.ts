import { h, resolveComponent } from 'vue'

const workManage = {
  path: 'work',
  name: '업무 관리',
  redirect: '/work/mytask',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'mytask',
      name: '내 페이지',
      component: () => import('@/views/_WorkManage/MyTask/Index.vue'),
      meta: { title: '내 페이지', auth: true },
    },
    {
      path: 'projects',
      name: '프로젝트',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '프로젝트', auth: true },
    },
    {
      path: 'admin',
      name: '관리 메뉴',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
      meta: { title: '관리 메뉴', auth: true },
    },
  ],
}

export default workManage
