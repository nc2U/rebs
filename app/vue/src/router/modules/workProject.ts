import { h, resolveComponent } from 'vue'

const workProject = {
  path: 'work',
  name: '업 무 관 리',
  redirect: '/work/project',
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
    {
      path: 'activity',
      name: '작업내역',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'issues',
      name: '업무',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'time_entries',
      name: '소요시간',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'gantt',
      name: '차트',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'calendar',
      name: '달력',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'news',
      name: '공지',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'documents',
      name: '문서',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'wiki',
      name: '위키',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'files',
      name: '파일',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'repository',
      name: '저장소',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
    {
      path: 'settings',
      name: '설정',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
      meta: { title: '업 무 관 리', auth: true },
    },
  ],
}

export default workProject
