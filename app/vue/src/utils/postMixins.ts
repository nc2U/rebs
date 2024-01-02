import { ref } from 'vue'
import { useDocument } from '@/store/pinia/document'

const docStore = useDocument()

export const items = ref([
  { title: '복사하기', icon: 'content-copy' },
  { title: '이동하기', icon: 'folder-arrow-right' },
  { title: '카테고리변경', icon: 'tag-multiple' },
  { title: '비밀글로', icon: 'lock' },
  { title: '댓글감춤', icon: 'comment-off' },
  { title: '공지올림', icon: 'bullhorn-variant' },
  { title: '블라인드처리', icon: 'eye-off' },
  { title: '휴지통으로', icon: 'trash-can' },
])

const copyPost = () => {
  // 게시판 목록 모달 띄우기
  alert('게시판 목록(라디오) -> 복사 버튼')
}

const movePost = () => {
  // 게시판 목록 모달 띄우기
  alert('게시판 목록(라디오) -> 이동 버튼')
}

const changeCategory = (board: number) => {
  // 게시판별 카테고리 목록 모달 띄우기
  alert(board + '카테고리 모달')
}

const toSecretPost = () => {
  const is_noticed = true
  if (!is_noticed) alert('이 게시글을 비밀글로 변경하였습니다.')
  else alert('이 게시글을 비밀글에서 해제하였습니다.')
}

const hideComments = () => {
  const is_noticed = true
  if (!is_noticed) alert('이 게시글의 댓글을 감춤 처리하였습니다.')
  else alert('이 게시글의 댓글 감춤을 해제하였습니다.')
}

const toNoticeUp = () => {
  const is_noticed = true
  if (!is_noticed) alert('이 게시글을 블라인드 처리하였습니다.')
  else alert('이 게시글을 공지에서 해제하였습니다.')
}

const toBlind = () => {
  const is_blinded = true
  if (!is_blinded) alert('이 게시글을 공지로 등록하였습니다.')
  else alert('이 게시글을 블라인드 해제하였습니다.')
}

const toTrashCan = () => {
  const is_soft_delete = true
  if (!is_soft_delete) {
    if (confirm('이 글을 휴지통으로 이동하시겠습니까?')) alert('soft delete 실행')
  } else {
    if (confirm('이 글을 휴지통에서 복구 하시겠습니까?')) alert('soft delete 해제 실행')
  }
}

export const toPostBlame = (pk: number) => alert('mixin - 준비중!')

export const toPostManage = (f: number, pk: number) => {
  if (f === 1) return copyPost()
  if (f === 2) return movePost()
  if (f === 3) return changeCategory(1)
  if (f === 4) return toSecretPost()
  if (f === 5) return hideComments()
  if (f === 6) return toNoticeUp()
  if (f === 7) return toBlind()
  if (f === 8) return toTrashCan()
}
