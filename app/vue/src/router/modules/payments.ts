import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.payment > '0'),
)

const payments = {
  path: 'payments',
  name: '분양 수납 관리',
  redirect: '/payments/index',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'index',
      name: '전체 납부 내역',
      component: () =>
        pageViewAuth.value
          ? import('@/views/payments/List/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '전체 납부 내역', auth: true },
    },
    {
      path: 'manage',
      name: '건별 수납 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/payments/Register/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '건별 수납 관리', auth: true },
    },
    {
      path: 'status',
      name: '수납 현황 집계',
      component: () =>
        pageViewAuth.value
          ? import('@/views/payments/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '수납 현황 집계', auth: true },
    },
  ],
}

export default payments
