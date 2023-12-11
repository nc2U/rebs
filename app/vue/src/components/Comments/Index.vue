<script lang="ts" setup="">
import { ref, type PropType } from 'vue'
import { useDocument } from '@/store/pinia/document'
import type { Comment } from '@/store/types/document'
import CommentList from './components/CommentList.vue'
import CommentForm from './components/CommentForm.vue'

defineProps({
  post: { type: Number, required: true },
  comments: { type: Array as PropType<Comment[]>, default: () => [] },
})

const formVision = ref<boolean>(true)
const actFormNum = ref<number | null>(null)

const docStore = useDocument()
const createComment = (payload: Comment) => docStore.createComment(payload)
const patchComment = (payload: Comment) => docStore.patchComment(payload)

const onSubmit = (payload: Comment) => {
  if (!payload?.pk) createComment(payload)
  else patchComment(payload)
}

const visionToggle = (payload: { num: number; sts: boolean }) => {
  formVision.value = payload.sts
  if (!payload.sts) actFormNum.value = payload.num
}
</script>

<template>
  <CommentList :act-form="actFormNum" :comments="comments" @vision-toggle="visionToggle" />
  <div v-show="formVision">
    <CommentForm :form-vision="formVision" :post="post" @on-submit="onSubmit" />
  </div>
</template>
