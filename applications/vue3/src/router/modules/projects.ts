import { h, resolveComponent } from 'vue'

const projects = {
  path: 'project',
  name: '신규 프로젝트',
  redirect: '/project/manage',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'manage',
      name: '프로젝트 관리',
      component: () => import('@/views/projects/List/Index.vue'),
    },
    {
      path: 'settings',
      name: '세부설정 관리',
      redirect: '/project/settings/order',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'order',
          name: '차수분류 등록',
          component: () => import('@/views/projects/OrderGroup/Index.vue'),
        },
        {
          path: 'type',
          name: '타입정보 등록',
          component: () => import('@/views/projects/Type/Index.vue'),
        },
        {
          path: 'floor',
          name: '층별조건 등록',
          component: () => import('@/views/projects/Floor/Index.vue'),
        },
        {
          path: 'price',
          name: '공급가격 등록',
          component: () => import('@/views/projects/Price/Index.vue'),
        },
        {
          path: 'payment-order',
          name: '납부회차 등록',
          component: () => import('@/views/projects/PayOrder/Index.vue'),
        },
        {
          path: 'down-payment',
          name: '계약조건 등록',
          component: () => import('@/views/projects/DownPay/Index.vue'),
        },
      ],
    },
    {
      path: 'site',
      name: '사업부지 관리',
      redirect: '/project/site/index',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'index',
          name: '지번목록 관리',
          component: () => import('@/views/projects/SiteList/Index.vue'),
        },
        {
          path: 'owner',
          name: '소유자별 관리',
          component: () => import('@/views/projects/SiteOwner/Index.vue'),
        },
        {
          path: 'contract',
          name: '매입계약 관리',
          component: () => import('@/views/projects/SiteContract/Index.vue'),
        },
      ],
    },
  ],
}

export default projects
