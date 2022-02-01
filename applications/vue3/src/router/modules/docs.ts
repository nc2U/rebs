import { h, resolveComponent } from 'vue'

const docs = {
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
      component: () => import('@/views/docs/GeneralDocs/Index.vue'),
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
          component: () => import('@/views/docs/LawsuitDocs/Index.vue'),
        },
        {
          path: 'case',
          name: '본사 소송사건',
          component: () => import('@/views/docs/LawsuitCase/Index.vue'),
        },
      ],
    },
  ],
}

export default docs
