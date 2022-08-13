import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/accounts'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.project > '0'),
)

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
      redirect: '/project/manage/index',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'index',
          name: '프로젝트 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/List/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '프로젝트 등록' },
        },
        {
          path: 'order',
          name: '차수분류 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/OrderGroup/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '차수분류 등록' },
        },
        {
          path: 'type',
          name: '타입정보 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/Type/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '타입정보 등록' },
        },
        {
          path: 'floor',
          name: '층별조건 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/Floor/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '층별조건 등록' },
        },
      ],
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
          path: 'bldg',
          name: '동(건물) 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/Building/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '동(건물) 등록' },
        },
        {
          path: 'unit',
          name: '호(유닛) 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/Unit/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '호(유닛) 등록' },
        },
        {
          path: 'price',
          name: '공급가격 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/Price/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '공급가격 등록' },
        },
        {
          path: 'payment-order',
          name: '납부회차 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/PayOrder/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '납부회차 등록' },
        },
        {
          path: 'down-payment',
          name: '계약조건 등록',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/DownPay/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '계약조건 등록' },
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
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/SiteList/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '지번목록 관리' },
        },
        {
          path: 'owner',
          name: '소유자별 관리',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/SiteOwner/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '소유자별 관리' },
        },
        {
          path: 'contract',
          name: '매입계약 관리',
          component: () =>
            pageViewAuth.value
              ? import('@/views/projects/SiteContract/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '매입계약 관리' },
        },
      ],
    },
  ],
}

export default projects
