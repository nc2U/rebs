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
    },
    {
      path: 'own-scrap',
      name: '스크랩',
      component: () => import('@/views/_MyPage/OwnScrap/Index.vue'),
      meta: { title: '스크랩', auth: true, except: true },
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
