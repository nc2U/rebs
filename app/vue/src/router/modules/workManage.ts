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
}

export default workManage
