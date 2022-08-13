import { computed, h, resolveComponent } from 'vue'
import { useAccount } from '@/store/pinia/accounts'

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
      path: 'employee',
      name: '직원정보 관리',
      component: () =>
        pageViewAuth.value
          ? import('@/views/hrManage/Employee/Index.vue')
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
    // {
    //   path: 'rank',
    //   name: '직급정보 관리'
    // }
  ],
}

export default hrManage
