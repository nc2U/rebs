import { computed, ref } from 'vue'
import { type PostFilter, useDocument } from '@/store/pinia/document'
import type { PatchPost } from '@/store/types/document'
import { message } from '@/utils/helper'

const docStore = useDocument()
const patchPost = (payload: PatchPost & { filter: PostFilter }) => docStore.patchPost(payload)
const patchPostLike = (pk: number) => docStore.patchPostLike(pk)
const patchPostBlame = (pk: number) => docStore.patchPostBlame(pk)

const patchCommentLike = (pk: number, post: number, page?: number) =>
  docStore.patchCommentLike(pk, post, page)
const patchCommentBlame = (pk: number, post: number, page?: number) =>
  docStore.patchCommentBlame(pk, post, page)

export const toPrint = (title: string) => {
  // Clone the specific area to be printed
  const printContent: any = document.getElementById('print-area')?.cloneNode(true)

  // Create a new window for printing
  const printWindow = window.open('', '_blank')
  if (printWindow) {
    printWindow.document.open()

    // Add the cloned content to the new window
    printWindow.document.write(`<html><head><title>${title}</title></head><body>`)
    printWindow.document.write(printContent?.innerHTML)
    printWindow.document.write('</body></html>')

    // Close the document for writing
    printWindow.document.close()

    // Print the new window
    printWindow.print()
    // Close the new window after printing
    printWindow.close()
  }
}

export const toPostLike = (pk: number) => patchPostLike(pk)

export const toPostBlame = (pk: number) => patchPostBlame(pk)

export const toCommentLike = (pk: number, post: number, page = 1) =>
  patchCommentLike(pk, post, page)

export const toCommentBlame = (pk: number, post: number, page = 1) =>
  patchCommentBlame(pk, post, page)

const is_secret = computed(() => docStore.post?.is_secret)
const secretTitle = computed(() => (is_secret.value ? '비밀글 해제' : '비밀글로'))
const secretIcon = computed(() => (is_secret.value ? 'lock-open-variant' : 'lock'))

export const postManageItems = computed(() => [
  { title: '복사하기', icon: 'content-copy' },
  { title: '이동하기', icon: 'folder-arrow-right' },
  { title: '카테고리변경', icon: 'tag-multiple' },
  { title: secretTitle.value, icon: secretIcon.value },
  { title: '댓글감춤', icon: 'comment-off' },
  { title: '공지올림', icon: 'bullhorn-variant' },
  { title: '블라인드처리', icon: 'eye-off' },
  { title: '휴지통으로', icon: 'trash-can' },
])

const toSecretPost = (post: number, state: boolean) =>
  patchPost({
    pk: post,
    is_secret: !state,
    filter: {},
  }).then(() =>
    message(
      'success',
      '',
      `게시글을 비밀글${!is_secret.value ? '에서 해제' : '로 변경'}하였습니다.`,
    ),
  )

const hideComments = (post: number, state: boolean) => {
  if (!state) alert('이 게시글의 댓글을 감춤 처리하였습니다.')
  else alert('이 게시글의 댓글 감춤을 해제하였습니다.')
}

const toNoticeUp = (post: number, state: boolean) => {
  if (!state) alert('이 게시글을 블라인드 처리하였습니다.')
  else alert('이 게시글을 공지에서 해제하였습니다.')
}

const toBlind = (post: number, state: boolean) => {
  if (!state) alert('이 게시글을 공지로 등록하였습니다.')
  else alert('이 게시글을 블라인드 해제하였습니다.')
}

const toTrashCan = (post: number, state: boolean) => {
  if (!state) {
    if (confirm('이 글을 휴지통으로 이동하시겠습니까?')) alert('soft delete 실행')
  } else {
    if (confirm('이 글을 휴지통에서 복구 하시겠습니까?')) alert('soft delete 해제 실행')
  }
}

export const toPostManage = (
  f: number,
  brd: number,
  cate: number | null,
  post: number,
  state = false,
) => {
  if (f === 4) return toSecretPost(post, state)
  if (f === 5) return hideComments(post, state)
  if (f === 6) return toNoticeUp(post, state)
  if (f === 7) return toBlind(post, state)
  if (f === 8) return toTrashCan(post, state)
}
