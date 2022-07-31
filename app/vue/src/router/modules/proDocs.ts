import store from '@/store'
import { h, resolveComponent } from 'vue'

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
        store.state.accounts.userInfo.is_superuser ||
        store.state.accounts.userInfo.staffauth?.project_docs > '0'
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
            store.state.accounts.userInfo.is_superuser ||
            store.state.accounts.userInfo.staffauth?.project_docs > '0'
              ? import('@/views/proDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송문서' },
        },
        {
          path: 'case',
          name: '현장 소송사건',
          component: () =>
            store.state.accounts.userInfo.is_superuser ||
            store.state.accounts.userInfo.staffauth?.project_docs > '0'
              ? import('@/views/proDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
          meta: { title: '현장 소송사건' },
        },
      ],
    },
  ],
}

export default proDocs
