import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const compViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.company_settings > '0'),
)

const authViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.auth_manage > '0'),
)

const settings = {
  path: 'settings',
  name: '환 경 설 정',
  redirect: '/settings/company',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'company',
      name: '회사 정보 관리',
      component: () =>
        compViewAuth.value
          ? import('@/views/settings/Company/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '회사 정보 관리' },
    },
    {
      path: 'authorization',
      name: '권한 설정 관리',
      component: () =>
        authViewAuth.value
          ? import('@/views/settings/Authorization/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '권한 설정 관리' },
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
