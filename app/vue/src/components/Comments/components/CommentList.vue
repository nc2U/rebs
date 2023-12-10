<script lang="ts" setup="">
import type { PropType } from 'vue'
import type { Comment as Cm } from '@/store/types/document'
import Comment from './Comment.vue'

defineProps({
  commentList: { type: Array as PropType<Cm[]>, default: () => [] },
})
</script>

<template>
  <div v-if="commentList.length">
    <h5 class="my-4 ml-4">{{ commentList.length }} Comments</h5>
    <ul class="comments mx-5 mb-4">
      <li v-for="comment in commentList" :key="comment.pk">
        <Comment :comment="comment" />
      </li>
    </ul>
  </div>
</template>
