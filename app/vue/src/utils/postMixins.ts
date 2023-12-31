import { useDocument } from '@/store/pinia/document'

const docStore = useDocument()

export const copyPost = () => {
  // 게시판 목록 모달 띄우기
  alert('게시판 목록(라디오) -> 복사 버튼')
}

export const movePost = () => {
  // 게시판 목록 모달 띄우기
  alert('게시판 목록(라디오) -> 이동 버튼')
}

export const changeCategory = (board: number) => {
  // 게시판별 카테고리 목록 모달 띄우기
  alert(board + '카테고리 모달')
}

export const toSecretPost = () => {
  const is_noticed = true
  if (!is_noticed) alert('이 게시글을 비밀글로 변경하였습니다.')
  else alert('이 게시글을 비밀글에서 해제하였습니다.')
}

export const hideComments = () => {
  const is_noticed = true
  if (!is_noticed) alert('이 게시글의 댓글을 감춤 처리하였습니다.')
  else alert('이 게시글의 댓글 감춤을 해제하였습니다.')
}

export const toNoticeUp = () => {
  const is_noticed = true
  if (!is_noticed) alert('이 게시글을 블라인드 처리하였습니다.')
  else alert('이 게시글을 공지에서 해제하였습니다.')
}

export const toBlind = () => {
  const is_blinded = true
  if (!is_blinded) alert('이 게시글을 공지로 등록하였습니다.')
  else alert('이 게시글을 블라인드 해제하였습니다.')
}

export const toTrashCan = () => {
  const is_soft_delete = true
  if (!is_soft_delete) {
    if (confirm('이 글을 휴지통으로 이동하시겠습니까?')) alert('soft delete 실행')
  } else {
    if (confirm('이 글을 휴지통에서 복구 하시겠습니까?')) alert('soft delete 해제 실행')
  }
}
