<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import { useDocument } from '@/store/pinia/document'
import type { Comment } from '@/store/types/document'
import CommentList from './components/CommentList.vue'
import CommentForm from './components/CommentForm.vue'

const props = defineProps({
  post: { type: Number, required: true },
  comments: { type: Array as PropType<Comment[]>, default: () => [] },
})

const formVision = ref<boolean>(true)
const actForm = ref<number | undefined>(undefined)

const docStore = useDocument()
const createComment = (payload: Comment) => docStore.createComment(payload)
const patchComment = (payload: Comment) => docStore.patchComment(payload)

const toLike = (payload: { pk: number; like: boolean }) => {
  if (payload.like) {
    alert('취소 로직 실행!')
    // profile patch -> like_comment -> pk 제거
    // comment -> like -= 1
  } else {
    alert('좋아요 로직 실행')
    // profile patch -> like_comment -> pk 추가
    // comment -> like += 1
  }
}

const onSubmit = (payload: Comment) => {
  console.log(payload)
  if (!payload?.pk) createComment(payload)
  else patchComment(payload)
}
const formReset = () => {
  formVision.value = true
  actForm.value = undefined
}

const visionToggle = (payload: { num: number; sts: boolean }) => {
  formVision.value = payload.sts
  if (!payload.sts) actForm.value = payload.num
}

const pageSelect = (page: number) => docStore.fetchCommentList(props.post, page)
</script>

<template>
  <CommentList
    :act-form="actForm"
    :comments="comments"
    @vision-toggle="visionToggle"
    @to-like="toLike"
    @on-submit="onSubmit"
    @form-reset="formReset"
    @page-select="pageSelect"
  />
  <div v-show="formVision">
    <CommentForm :form-vision="formVision" :post="post" @on-submit="onSubmit" />
  </div>
</template>
