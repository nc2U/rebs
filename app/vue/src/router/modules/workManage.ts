import { h, resolveComponent } from 'vue'

const workManage = {
  path: 'admin',
  name: '설 정 관 리',
  redirect: '/admin/projects',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  meta: { title: '설 정 관 리', auth: true },
  children: [
    {
      path: 'projects',
      name: '프로젝트 관리',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'users',
      name: '사용자',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'groups',
      name: '그룹',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'roles',
      name: '역할 및 권한',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'trackers',
      name: '작업 유형',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'statuses',
      name: '작업 상태',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'workflows',
      name: '업무 흐름',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'custom_fields',
      name: '사용자 정의 항목',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'enumerations',
      name: '코드값',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'settings',
      name: '제반 설정',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'auth_sources',
      name: 'LDAP 인증',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'plugins',
      name: '플러그인',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
    {
      path: 'info',
      name: '정보',
      component: () => import('@/views/_WorkManage/Admin/Index.vue'),
    },
  ],
}

export default workManage
