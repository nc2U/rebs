import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/accounts'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.company_settings > '0'),
)

const settings = {
  path: 'settings',
  name: '환경설정',
  redirect: '/settings/company',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'company',
      name: '회사정보 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/settings/Company/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '회사정보 관리' },
    },
    {
      path: 'authorization',
      name: '권한설정 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/settings/Authorization/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '권한설정 관리' },
    },
    {
      path: 'profile',
      name: '프로필 관리',
      component: () => import('@/views/settings/Profile/Index.vue'),
      meta: { title: '프로필 관리' },
    },
  ],
}

export default settings
