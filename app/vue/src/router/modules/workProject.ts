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
  meta: { title: '업 무 관 리', auth: true, affix: true },
  children: [
    {
      path: 'project',
      name: '프로젝트',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'activity',
      name: '작업내역',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'issues',
      name: '업무',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'time_entries',
      name: '소요시간',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'gantt',
      name: '차트',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'calendar',
      name: '달력',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'news',
      name: '공지',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'documents',
      name: '문서',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'wiki',
      name: '위키',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'files',
      name: '파일',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'repository',
      name: '저장소',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
    {
      path: 'settings',
      name: '설정',
      component: () => import('@/views/_WorkManage/Project/Index.vue'),
    },
  ],
}

export default workProject
