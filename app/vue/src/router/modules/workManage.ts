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
        {
          path: 'users',
          name: '사용자',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'groups',
          name: '그룹',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'roles',
          name: '역할 및 권한',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'trackers',
          name: '작업 유형',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'statuses',
          name: '작업 상태',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'workflows',
          name: '업무 흐름',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'custom_fields',
          name: '사용자 정의 항목',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'enumerations',
          name: '코드값',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'settings',
          name: '제반 설정',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'auth_sources',
          name: 'LDAP 인증',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'plugins',
          name: '플러그인',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
        {
          path: 'info',
          name: '정보',
          component: () => import('@/views/_WorkManage/Admin/Index.vue'),
          meta: { title: '설 정 관 리', auth: true },
        },
      ],
    },
  ],
}

export default workManage
