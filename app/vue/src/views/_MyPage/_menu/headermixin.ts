import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'

const accStore = useAccount()
const superAuth = computed(() => accStore.superAuth)

export const pageTitle = '마이 페이지'
export const navMenu = superAuth.value
  ? ['내 정보', '할일 관리', '내 작성글', '스크랩', '휴지통', '정보 수정', '탈퇴 하기']
  : ['내 정보', '할일 관리', '내 작성글', '스크랩', '정보 수정', '탈퇴 하기']
