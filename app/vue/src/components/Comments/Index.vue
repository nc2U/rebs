<script lang="ts" setup="">
import type { PropType } from 'vue'
import { useDocument } from '@/store/pinia/document'
import type { Comment } from '@/store/types/document'
import CommentList from './components/CommentList.vue'
import CommentForm from './components/CommentForm.vue'

defineProps({
  post: { type: Number, required: true },
  comments: { type: Array as PropType<Comment[]>, default: () => [] },
})

const docStore = useDocument()
const createComment = (payload: Comment) => docStore.createComment(payload)
const patchComment = (payload: Comment) => docStore.patchComment(payload)

const onSubmit = (payload: Comment) => {
  if (!payload?.pk) createComment(payload)
  else patchComment(payload)
}
</script>

<template>
  <CommentList :comments="comments" />
  <CommentForm :post="post" @on-submit="onSubmit" />
</template>
