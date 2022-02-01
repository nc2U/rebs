import { h, resolveComponent } from 'vue'

const cashes = {
  path: 'cashes',
  name: '본사회계 관리',
  redirect: '/cashes/status',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'status',
      name: '본사자금 현황',
      component: () => import('@/views/cashes/Status/Index.vue'),
    },
    {
      path: 'index',
      name: '본사입출 내역',
      component: () => import('@/views/cashes/List/Index.vue'),
    },
    {
      path: 'register',
      name: '본사입출 등록',
      component: () => import('@/views/cashes/Register/Index.vue'),
    },
  ],
}

export default cashes
