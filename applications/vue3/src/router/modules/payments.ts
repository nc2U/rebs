import { h, resolveComponent } from 'vue'

const payments = {
  path: 'payments',
  name: '분양수납 관리',
  redirect: '/payments/index',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'index',
      name: '분양수납 내역',
      component: () => import('@/views/payments/List/Index.vue'),
    },
    {
      path: 'manage',
      name: '건별수납 관리',
      component: () => import('@/views/payments/Register/Index.vue'),
    },
  ],
}

export default payments
