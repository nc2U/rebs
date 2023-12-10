<script lang="ts" setup="">
import { computed } from 'vue'
import { useDocument } from '@/store/pinia/document'
import type { Comment } from '@/store/types/document'
import CommentList from './components/CommentList.vue'
import CommentForm from './components/CommentForm.vue'

const props = defineProps({ post: { type: Number, required: true } })

const docStore = useDocument()
const commentList = computed(() => docStore.commentList)

const createComment = (payload: Comment) => docStore.createComment(payload)
const patchComment = (payload: Comment) => docStore.patchComment(payload)

const onSubmit = (payload: Comment) => {
  payload.post = props.post
  console.log(payload)

  if (!payload?.pk) createComment(payload)
  else patchComment(payload)
}
</script>

<template>
  <CommentList :comment-list="commentList" />
  <CommentForm @on-submit="onSubmit" />
</template>
