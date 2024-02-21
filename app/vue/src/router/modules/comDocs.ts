import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth && account.value.userInfo.staffauth?.company_docs > '0'),
)

const comDocs = {
  path: 'docs',
  name: '본사 문서 관리',
  redirect: '/docs/general/posts',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'general/posts',
      name: '본사 일반 문서',
      component: () =>
        pageViewAuth.value
          ? import('@/views/comDocs/GeneralDocs/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '본사 일반 문서', auth: true },
      children: [
        {
          path: ':postId(\\d+)',
          name: '본사 일반 문서 - 보기',
        },
        {
          path: ':postId(\\d+)/update',
          name: '본사 일반 문서 - 수정',
        },
        {
          path: 'create',
          name: '본사 일반 문서 - 작성',
        },
      ],
    },
    {
      path: 'official/letters',
      name: '본사 공문 발송',
      component: () =>
        pageViewAuth.value
          ? import('@/views/comDocs/OfficialLetter/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '본사 공문 발송', auth: true },
      children: [
        {
          path: ':postId(\\d+)',
          name: '본사 공문 발송 - 보기',
        },
        {
          path: ':postId(\\d+)/update',
        },
        {
          path: 'create',
          name: '본사 공문 발송 - 작성',
        },
      ],
    },
    {
      path: 'lawsuit',
      name: '본사 소송 관리',
      redirect: '/docs/lawsuit/posts',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'posts',
          name: '본사 소송 문서',
          component: () =>
            pageViewAuth.value
              ? import('@/views/comDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '본사 소송 문서', auth: true },
          children: [
            {
              path: ':postId(\\d+)',
              name: '본사 소송 문서 - 보기',
            },
            {
              path: ':postId(\\d+)/update',
              name: '본사 소송 문서 - 수정',
            },
            {
              path: 'create',
              name: '본사 소송 문서 - 작성',
            },
          ],
        },
        {
          path: 'case',
          name: '본사 소송 사건',
          component: () =>
            pageViewAuth.value
              ? import('@/views/comDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '본사 소송 사건', auth: true },
          children: [
            {
              path: ':caseId(\\d+)',
              name: '본사 소송 사건 - 보기',
            },
            {
              path: ':caseId(\\d+)/update',
              name: '본사 소송 사건 - 수정',
            },
            {
              path: 'create',
              name: '본사 소송 사건 - 작성',
            },
          ],
        },
      ],
    },
  ],
}

export default comDocs
