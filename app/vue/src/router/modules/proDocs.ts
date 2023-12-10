import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth && account.value.userInfo.staffauth?.project_docs > '0'),
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
      meta: { title: '현장 일반 문서', auth: true },
      children: [
        {
          path: ':postId(\\d+)',
          name: '현장 일반 문서 - 보기',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/GeneralDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 일반 문서', auth: true, except: true },
        },
        {
          path: ':postId(\\d+)/update',
          name: '현장 일반 문서 - 수정',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/GeneralDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 일반 문서', auth: true, except: true },
        },
        {
          path: 'create',
          name: '현장 일반 문서 - 작성',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/GeneralDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 일반 문서', auth: true, except: true },
        },
      ],
    },
    {
      path: 'lawsuit/posts',
      name: '현장 소송 문서',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proDocs/LawsuitDocs/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '현장 소송 문서', auth: true },
      children: [
        {
          path: ':postId(\\d+)',
          name: '현장 소송 문서 - 보기',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 문서', auth: true, except: true },
        },
        {
          path: ':postId(\\d+)/update',
          name: '현장 소송 문서 - 수정',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 문서', auth: true, except: true },
        },
        {
          path: 'create',
          name: '현장 소송 문서 - 작성',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 문서', auth: true, except: true },
        },
      ],
    },
    {
      path: 'lawsuit/case',
      name: '현장 소송 사건',
      component: () =>
        pageViewAuth.value
          ? import('@/views/proDocs/LawsuitCase/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '현장 소송 사건', auth: true },
      children: [
        {
          path: ':caseId(\\d+)',
          name: '현장 소송 사건 - 보기',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 사건', auth: true, except: true },
        },
        {
          path: ':caseId(\\d+)/update',
          name: '현장 소송 사건 - 수정',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 사건', auth: true, except: true },
        },
        {
          path: 'create',
          name: '현장 소송 사건 - 작성',
          component: () =>
            pageViewAuth.value
              ? import('@/views/proDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송 사건', auth: true, except: true },
        },
      ],
    },
  ],
}

export default proDocs