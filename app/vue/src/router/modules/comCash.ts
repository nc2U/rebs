import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.company_cash > '0'),
)

const comCash = {
  path: 'cashes',
  name: '본사회계 관리',
  redirect: '/cashes/status',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'status',
      name: '본사자금 현황',
      component: () =>
        pageViewAuth.value
          ? import('@/views/comCash/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '본사자금 현황' },
    },
    {
      path: 'index',
      name: '본사출납 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/comCash/Manage/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '본사출납 관리' },
    },
  ],
}

export default comCash
