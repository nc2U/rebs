import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.contract > '0'),
)

const contract = {
  path: 'contracts',
  name: '분양계약 관리',
  redirect: '/contracts/index',
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
        pageViewAuth.value
          ? import('@/views/contracts/List/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '계약내역 조회' },
    },
    {
      path: 'register',
      name: '계약등록 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/contracts/Register/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '계약등록 관리' },
    },
    {
      path: 'status',
      name: '동호수 현황표',
      component: () =>
        pageViewAuth.value
          ? import('@/views/contracts/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '동호수 현황표' },
    },
    {
      path: 'cancel',
      name: '계약해지 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/contracts/Release/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '계약해지 관리' },
    },
  ],
}

export default contract
