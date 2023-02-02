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
  name: '현장 문서 관리',
  redirect: '/project-docs/general/posts',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'general/posts',
      name: '현장 일반 문서',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proDocs/GeneralDocs/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '현장 일반 문서' },
    },
    {
      path: 'official/letters',
      name: '현장 공문 발송',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proDocs/OfficialLetter/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '현장 공문 발송' },
    },
    {
      path: 'lawsuit',
      name: '현장 소송 관리',
      redirect: '/project-docs/lawsuit/posts',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'posts',
          name: '현장 소송 문서',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 문서' },
        },
        {
          path: 'case',
          name: '현장 소송 사건',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 사건' },
        },
      ],
    },
  ],
}

export default proDocs
