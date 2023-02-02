import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.notice > '0'),
)

const notices = {
  path: 'notices',
  name: '고객 고지 관리',
  redirect: '/notices/bill',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'bill',
      name: '수납 고지서 출력',
      component: () =>
        pageViewAuth.value
          ? import('@/views/notices/Bill/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '수납 고지서 출력' },
    },
    {
      path: 'sms',
      name: 'SMS 발송 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/notices/Sms/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: 'SMS 발송 관리' },
    },
    {
      path: 'mailing',
      name: 'MAIL 발송 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/notices/Mailing/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: 'MAIL 발송 관리' },
    },
    {
      path: 'post-label',
      name: '우편 라벨 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/notices/Label/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '우편 라벨 관리' },
    },
    {
      path: 'log',
      name: '발송 기록 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/notices/Log/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '발송 기록 관리' },
    },
  ],
}

export default notices
