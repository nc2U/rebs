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
const actForm = ref<number | undefined>(undefined)

const docStore = useDocument()
const createComment = (payload: Comment) => docStore.createComment(payload)
const patchComment = (payload: Comment) => docStore.patchComment(payload)

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
</script>

<template>
  <CommentList
    :act-form="actForm"
    :comments="comments"
    @vision-toggle="visionToggle"
    @on-submit="onSubmit"
    @form-reset="formReset"
  />
  <div v-show="formVision">
    <CommentForm :form-vision="formVision" :post="post" @on-submit="onSubmit" />
  </div>
</template>
