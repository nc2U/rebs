import { h, resolveComponent } from 'vue'

const projectDocs = {
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
      component: () => import('@/views/projectDocs/GeneralDocs/Index.vue'),
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
          component: () => import('@/views/projectDocs/LawsuitDocs/Index.vue'),
        },
        {
          path: 'case',
          name: '현장 소송사건',
          component: () => import('@/views/projectDocs/LawsuitCase/Index.vue'),
        },
      ],
    },
  ],
}

export default projectDocs
