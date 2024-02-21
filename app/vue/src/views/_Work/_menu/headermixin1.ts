import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'

const accStore = useAccount()
const superAuth = computed(() => accStore.superAuth)

export const pageTitle = '업 무 관 리'
export const navMenu1 = ['프로젝트', '작업내역', '업무', '소요시간', '차트', '달력', '공지']

export const navMenu2 = superAuth?.value
  ? [
      '개요',
      '작업내역',
      '업무',
      '소요시간',
      '차트',
      '달력',
      '공지',
      '문서',
      '위키',
      '파일',
      '저장소',
      '설정',
    ]
  : [
      '개요',
      '작업내역',
      '업무',
      '소요시간',
      '차트',
      '달력',
      '공지',
      '문서',
      '위키',
      '파일',
      '저장소',
    ]
