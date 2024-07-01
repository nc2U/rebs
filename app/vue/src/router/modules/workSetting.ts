import { h, resolveComponent } from 'vue'

const workSetting = {
  path: 'manage',
  name: '설 정 관 리',
  redirect: '/manage/project',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  meta: { title: '설 정 관 리', auth: true },
  children: [
    {
      path: 'project',
      name: '(프로젝트)',
      component: () => import('@/views/_Work/Settings/Projects/Index.vue'),
    },
    {
      path: 'user',
      name: '사용자',
      component: () => import('@/views/_Work/Settings/Users/Index.vue'),
      children: [
        {
          path: ':userId',
          name: '사용자 - 보기',
        },
        {
          path: 'create',
          name: '사용자 - 생성',
        },
        {
          path: ':userId/update',
          name: '사용자 - 수정',
        },
      ],
    },
    // {
    //   path: 'group',
    //   name: '그룹',
    //   component: () => import('@/views/_Work/Settings/Groups/Index.vue'),
    // },
    {
      path: 'role',
      name: '역할 및 권한',
      component: () => import('@/views/_Work/Settings/Roles_Perms/Index.vue'),
    },
    {
      path: 'tracker',
      name: '업무 유형',
      component: () => import('@/views/_Work/Settings/Trackers/Index.vue'),
    },
    {
      path: 'status',
      name: '업무 상태',
      component: () => import('@/views/_Work/Settings/Statuses/Index.vue'),
    },
    {
      path: 'workflow',
      name: '업무 흐름',
      component: () => import('@/views/_Work/Settings/Workflow/Index.vue'),
    },
    // {
    //   path: 'custom_field',
    //   name: '사용자 정의 항목',
    //   component: () => import('@/views/_Work/Settings/CustomField/Index.vue'),
    // },
    {
      path: 'enumerate',
      name: '코드값',
      component: () => import('@/views/_Work/Settings/Enumerations/Index.vue'),
    },
    {
      path: 'setting',
      name: '제반 설정',
      component: () => import('@/views/_Work/Settings//Settings/Index.vue'),
    },
    // {
    //   path: 'auth_source',
    //   name: 'LDAP 인증',
    //   component: () => import('@/views/_Work/Settings/LDAPAuth/Index.vue'),
    // },
    // {
    //   path: 'plugin',
    //   name: '플러그인',
    //   component: () => import('@/views/_Work/Settings/PlugIn/Index.vue'),
    // },
    // {
    //   path: 'info',
    //   name: '정보',
    //   component: () => import('@/views/_Work/Settings/Info/Index.vue'),
    // },
  ],
}

export default workSetting
