import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/account'

const account = computed(() => useAccount())
const pageViewAuth = computed(
  () =>
    account.value.userInfo?.is_superuser ||
    (account.value.userInfo?.staffauth &&
      account.value.userInfo.staffauth?.human_resource > '0'),
)

const hrManage = {
  path: 'hr-manage',
  name: '본사인사 관리',
  redirect: '/hr-manage/employee',
  component: {
    render() {
      return h(resolveComponent('router-view'))
    },
  },
  children: [
    {
      path: 'staff',
      name: '직원정보 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/hrManage/Staff/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '직원정보 관리' },
    },
    {
      path: 'department',
      name: '부서정보 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/hrManage/Department/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '부서정보 관리' },
    },
    {
      path: 'position',
      name: '직위정보 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/hrManage/Position/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '직위정보 관리' },
    },
    {
      path: 'duty',
      name: '직책정보 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/hrManage/Duty/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '직책정보 관리' },
    },
    {
      path: 'grade',
      name: '직급정보 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/hrManage/Grade/Index.vue')
          : import('@/views/_Accounts/NoAuth.vue'),
      meta: { title: '직급정보 관리' },
    },
  ],
}

export default hrManage
