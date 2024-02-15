import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'

const accStore = useAccount()
const superAuth = computed(() => accStore.superAuth)

export const pageTitle = '업무 관리'
export const navMenu = superAuth.value
  ? ['내 페이지', '프로젝트', '관리 메뉴']
  : ['내 페이지', '프로젝트']
