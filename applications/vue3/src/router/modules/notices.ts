import { h, resolveComponent } from 'vue'

const notices = {
  path: 'notices',
  name: '고객고지 관리',
  redirect: '/notices/bill',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'bill',
      name: '수납고지서 출력',
      component: () => import('@/views/notices/Bill/Index.vue'),
    },
    {
      path: 'sms',
      name: 'SMS 발송관리',
      component: () => import('@/views/notices/Sms/Index.vue'),
    },
    {
      path: 'mailing',
      name: 'MAIL 발송관리',
      component: () => import('@/views/notices/Mailing/Index.vue'),
    },
    {
      path: 'post-label',
      name: '우편라벨 관리',
      component: () => import('@/views/notices/Label/Index.vue'),
    },
    {
      path: 'log',
      name: '발송기록 관리',
      component: () => import('@/views/notices/Log/Index.vue'),
    },
  ],
}

export default notices
