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
      path: 'task',
      name: '업 무 관 리',
      redirect: '/work/task/project',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'project',
          name: '프로젝트',
          component: () => import('@/views/_WorkManage/Project/Index.vue'),
          meta: { title: '업 무 관 리', auth: true },
        },
      ],
    },
    {
      path: 'admin',
      name: '설 정 관 리',
      redirect: '/work/admin/projects',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'projects',
          name: '프로젝트 관리',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
      ],
    },
  ],
}

export default workManage
