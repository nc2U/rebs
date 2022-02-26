import store from '@/store'
import { h, resolveComponent } from 'vue'

const comDocs = {
  path: 'docs',
  name: '본사문서 관리',
  redirect: '/docs/general/docs',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'general/docs',
      name: '본사 일반문서',
      component: () =>
        store.state.accounts.userInfo.staffauth.company_docs > '0'
          ? import('@/views/comDocs/GeneralDocs/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
    },
    {
      path: 'lawsuit',
      name: '본사 소송관리',
      redirect: '/docs/lawsuit/docs',
      component: {
        render() {
          return h(resolveComponent('router-view'))
        },
      },
      children: [
        {
          path: 'docs',
          name: '본사 소송문서',
          component: () =>
            store.state.accounts.userInfo.staffauth.company_docs > '0'
              ? import('@/views/comDocs/LawsuitDocs/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
        },
        {
          path: 'case',
          name: '본사 소송사건',
          component: () =>
            store.state.accounts.userInfo.staffauth.company_docs > '0'
              ? import('@/views/comDocs/LawsuitCase/Index.vue')
              : import('@/views/_Accounts/NoAuth.vue'),
        },
      ],
    },
  ],
}

export default comDocs
