import { h, resolveComponent } from 'vue'

const workSetting = {
  path: 'admin',
  name: '설 정 관 리',
  redirect: '/admin/project',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  meta: { title: '설 정 관 리', auth: true },
  children: [
    {
      path: 'project',
      name: '프로젝트 목록',
      component: () => import('@/views/_Work/Settings/Index.vue'),
    },
    {
      path: 'user',
      name: '사용자',
      component: () => import('@/views/_Work/Settings/components/Users/Index.vue'),
    },
    {
      path: 'group',
      name: '그룹',
      component: () => import('@/views/_Work/Settings/components/Groups/Index.vue'),
    },
    {
      path: 'role',
      name: '역할 및 권한',
      component: () => import('@/views/_Work/Settings/components/Roles_Perms/Index.vue'),
    },
    {
      path: 'tracker',
      name: '작업 유형',
      component: () => import('@/views/_Work/Settings/components/Trackers/Index.vue'),
    },
    {
      path: 'status',
      name: '작업 상태',
      component: () => import('@/views/_Work/Settings/components/Statuses/Index.vue'),
    },
    {
      path: 'workflow',
      name: '업무 흐름',
      component: () => import('@/views/_Work/Settings/components/Workflow/Index.vue'),
    },
    // {
    //   path: 'custom_field',
    //   name: '사용자 정의 항목',
    //   component: () => import('@/views/_Work/Settings/components//Index.vue'),
    // },
    {
      path: 'enumerate',
      name: '코드값',
      component: () => import('@/views/_Work/Settings/components/Enumerations/Index.vue'),
    },
    {
      path: 'setting',
      name: '제반 설정',
      component: () => import('@/views/_Work/Settings/components/Settings/Index.vue'),
    },
    // {
    //   path: 'auth_source',
    //   name: 'LDAP 인증',
    //   component: () => import('@/views/_Work/Settings/Index.vue'),
    // },
    // {
    //   path: 'plugin',
    //   name: '플러그인',
    //   component: () => import('@/views/_Work/Settings/Index.vue'),
    // },
    // {
    //   path: 'info',
    //   name: '정보',
    //   component: () => import('@/views/_Work/Settings/Index.vue'),
    // },
  ],
}

export default workSetting
