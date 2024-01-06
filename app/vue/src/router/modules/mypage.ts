import { h, resolveComponent } from 'vue'

const myPage = {
  path: 'mypage',
  name: '마이페이지',
  redirect: '/mypage/own-info',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'own-info',
      name: '내 정보',
      component: () => import('@/views/_MyPage/OwnInfo/Index.vue'),
      meta: { title: '내 정보', auth: true, except: true },
    },
    {
      path: 'todo-list',
      name: '할일 관리',
      component: () => import('@/views/_MyPage/MyTodoList/Index.vue'),
      meta: { title: '할일 관리', auth: true, except: true },
    },
    {
      path: 'own-post',
      name: '내 작성글',
      component: () => import('@/views/_MyPage/OwnPost/Index.vue'),
      meta: { title: '내 작성글', auth: true, except: true },
      children: [
        {
          path: ':postId(\\d+)',
          name: '내 작성글 - 보기',
          component: () => import('@/views/_MyPage/OwnPost/Index.vue'),
          meta: { title: '내 작성글', auth: true, except: true },
        },
        {
          path: ':postId(\\d+)/update',
          name: '내 작성글 - 수정',
          component: () => import('@/views/_MyPage/OwnPost/Index.vue'),
          meta: { title: '내 작성글', auth: true, except: true },
        },
        {
          path: 'create',
          name: '내 작성글 - 작성',
          component: () => import('@/views/_MyPage/OwnPost/Index.vue'),
          meta: { title: '내 작성글', auth: true, except: true },
        },
      ],
    },
    {
      path: 'own-scrap',
      name: '스크랩',
      component: () => import('@/views/_MyPage/OwnScrap/Index.vue'),
      meta: { title: '스크랩', auth: true, except: true },
      children: [
        {
          path: ':postId(\\d+)',
          name: '스크랩 - 보기',
          component: () => import('@/views/_MyPage/OwnScrap/Index.vue'),
          meta: { title: '스크랩', auth: true, except: true },
        },
        {
          path: ':postId(\\d+)/update',
          name: '스크랩 - 수정',
          component: () => import('@/views/_MyPage/OwnScrap/Index.vue'),
          meta: { title: '스크랩', auth: true, except: true },
        },
        {
          path: 'create',
          name: '스크랩 - 작성',
          component: () => import('@/views/_MyPage/OwnScrap/Index.vue'),
          meta: { title: '스크랩', auth: true, except: true },
        },
      ],
    },
    {
      path: 'trash-can',
      name: '휴지통',
      component: () => import('@/views/_MyPage/TrashCan/Index.vue'),
      meta: { title: '휴지통', auth: true, except: true },
      children: [
        {
          path: ':postId(\\d+)',
          name: '휴지통 - 보기',
          component: () => import('@/views/_MyPage/TrashCan/Index.vue'),
          meta: { title: '휴지통', auth: true, except: true },
        },
        {
          path: ':postId(\\d+)/update',
          name: '휴지통 - 수정',
          component: () => import('@/views/_MyPage/TrashCan/Index.vue'),
          meta: { title: '휴지통', auth: true, except: true },
        },
        {
          path: 'create',
          name: '휴지통 - 작성',
          component: () => import('@/views/_MyPage/TrashCan/Index.vue'),
          meta: { title: '휴지통', auth: true, except: true },
        },
      ],
    },
    {
      path: 'modify',
      name: '정보 수정',
      component: () => import('@/views/_MyPage/Modify/Index.vue'),
      meta: { title: '정보 수정', auth: true, except: true },
    },
    {
      path: 'secession',
      name: '탈퇴 하기',
      component: () => import('@/views/_MyPage/Secession/Index.vue'),
      meta: { title: '탈퇴 하기', auth: true, except: true },
    },
  ],
}

export default myPage
