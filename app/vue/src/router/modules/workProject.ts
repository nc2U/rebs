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
      component: () => import('@/views/_Work/Manages/Projects/Index.vue'),
      children: [
        {
          path: 'create',
          name: '프로젝트 - 추가',
        },
        // {
        //   path: ':projId/update',
        //   name: '프로젝트 - 수정',
        // },
        {
          path: ':projId/delete',
          name: '프로젝트 - 삭제',
        },
        {
          path: ':projId',
          name: '(개요)',
        },
        {
          path: ':projId/activity',
          name: '(작업내역)',
        },
        {
          path: ':projId/roadmap',
          name: '(로드맵)',
        },
        {
          path: ':projId/issue',
          name: '(업무)',
          children: [
            {
              path: ':issueId',
              name: '(업무) - 보기',
            },
            {
              path: 'create',
              name: '(업무) - 추가',
            },
            {
              path: ':issueId/update',
              name: '(업무) - 편집',
            },
            {
              path: ':issueId/delete',
              name: '(업무) - 삭제',
            },
          ],
        },
        {
          path: ':projId/time_entry',
          name: '(소요시간)',
        },
        {
          path: ':projId/gantt',
          name: '(차트)',
        },
        {
          path: ':projId/calendar',
          name: '(달력)',
        },
        {
          path: ':projId/news',
          name: '(공지)',
        },
        {
          path: ':projId/document',
          name: '(문서)',
        },
        {
          path: ':projId/wiki',
          name: '(위키)',
        },
        {
          path: ':projId/forum',
          name: '(게시판)',
        },
        {
          path: ':projId/file',
          name: '(파일)',
        },
        {
          path: ':projId/repository',
          name: '(저장소)',
        },
        {
          path: ':projId/setting',
          name: '(설정)',
        },
        {
          path: ':projId/search',
          name: '(검색)',
        },
      ],
    },
    {
      path: 'activity',
      name: '작업내역',
      component: () => import('@/views/_Work/Manages/Activity/Index.vue'),
    },
    {
      path: 'issue',
      name: '업무',
      component: () => import('@/views/_Work/Manages/Issues/Index.vue'),
      children: [
        {
          path: 'create',
          name: '업무 - 추가',
        },
      ],
    },
    {
      path: 'time_entry',
      name: '소요시간',
      component: () => import('@/views/_Work/Manages/SpentTime/Index.vue'),
    },
    {
      path: 'gantt',
      name: '차트',
      component: () => import('@/views/_Work/Manages/Gantt/Index.vue'),
    },
    {
      path: 'calendar',
      name: '달력',
      component: () => import('@/views/_Work/Manages/Calendar/Index.vue'),
    },
    {
      path: 'news',
      name: '공지',
      component: () => import('@/views/_Work/Manages/News/Index.vue'),
    },
    {
      path: 'search',
      name: '전체검색',
      component: () => import('@/views/_Work/components/SearchBody/Index.vue'),
    },
  ],
}

export default workProject
