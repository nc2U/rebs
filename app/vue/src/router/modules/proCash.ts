import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.project_cash > '0'),
)

const proCash = {
  path: 'project-cash',
  name: '현장자금 관리',
  redirect: '/project-cash/status',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'status',
      name: '현장자금 현황',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proCash/Status/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '현장자금 현황' },
    },
    {
      path: 'index',
      name: '현장출납 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proCash/Manage/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '현장출납 관리' },
    },
    {
      path: 'imprest',
      name: '운영비용 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proCash/Imprest/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '운영비용 관리' },
    },
  ],
}

export default proCash
