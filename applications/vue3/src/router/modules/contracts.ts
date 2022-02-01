import { h, resolveComponent } from 'vue'

const contract = {
  path: 'contracts',
  name: '분양계약 관리',
  redirect: '/contracts/info',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'info',
      name: '계약현황 조회',
      redirect: '/contracts/info/index',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'index',
          name: '계약내역 조회',
          component: () =>
            import(
              /* webpackPrefetch: true */ '@/views/contracts/List/Index.vue'
            ),
        },
        {
          path: 'status',
          name: '동호수 현황표',
          component: () => import('@/views/contracts/Status/Index.vue'),
        },
      ],
    },
    {
      path: 'manage',
      name: '계약정보 관리',
      redirect: '/contracts/manage/register',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'register',
          name: '계약등록 관리',
          component: () => import('@/views/contracts/Register/Index.vue'),
        },
        {
          path: 'cancel',
          name: '계약해지 관리',
          component: () => import('@/views/contracts/Cancel/Index.vue'),
        },
      ],
    },
  ],
}

export default contract
