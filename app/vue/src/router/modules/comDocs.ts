import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.company_docs > '0'),
)

const comDocs = {
  path: 'docs',
  name: '본사문서 관리',
  redirect: '/docs/general/posts',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'general/posts',
      name: '본사 일반문서',
      component: () =>
        pageViewAuth.value
          ? import('@/views/comDocs/GeneralDocs/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '본사 일반문서' },
    },
    {
      path: 'lawsuit',
      name: '본사 소송관리',
      redirect: '/docs/lawsuit/posts',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'posts',
          name: '본사 소송문서',
          component: () =>
            pageViewAuth.value
              ? import('@/views/comDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '본사 소송문서' },
        },
        {
          path: 'case',
          name: '본사 소송사건',
          component: () =>
            pageViewAuth.value
              ? import('@/views/comDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '본사 소송사건' },
        },
      ],
    },
  ],
}

export default comDocs
