import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.project_docs > '0'),
)

const proDocs = {
  path: 'project-docs',
  name: '현장문서 관리',
  redirect: '/project-docs/general/docs',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'general/docs',
      name: '현장 일반문서',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proDocs/GeneralDocs/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '현장 일반문서' },
    },
    {
      path: 'lawsuit',
      name: '현장 소송관리',
      redirect: '/project-docs/lawsuit/docs',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'docs',
          name: '현장 소송문서',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송문서' },
        },
        {
          path: 'case',
          name: '현장 소송사건',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송사건' },
        },
      ],
    },
  ],
}

export default proDocs
