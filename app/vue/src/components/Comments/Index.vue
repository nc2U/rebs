<script lang="ts" setup="">
import { computed } from 'vue'
import { useDocument } from '@/store/pinia/document'
import CommentList from './components/CommentList.vue'
import CommentForm from './components/CommentForm.vue'
import type { Comment } from '@/store/types/document'

const props = defineProps({ post: { type: Number, required: true } })

const docStore = useDocument()
const commentList = computed(() => docStore.commentList)

const onSubmit = (payload: Comment) => {
  payload.post = props.post
  console.log(payload)
}
</script>

<template>
  <CommentList :comment-list="commentList" />
  <CommentForm @on-submit="onSubmit" />
</template>
