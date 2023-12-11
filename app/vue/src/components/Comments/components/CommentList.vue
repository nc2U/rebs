<script lang="ts" setup="">
import type { PropType } from 'vue'
import type { Comment as Cm } from '@/store/types/document'
import Comment from './Comment.vue'

defineProps({
  comments: { type: Array as PropType<Cm[]>, default: () => [] },
})
</script>

<template>
  <div v-if="comments.length">
    <h5 class="my-4 ml-4">{{ comments.length }} Comments</h5>
    <ul class="comments mx-5 mb-4">
      <li v-for="cmt in comments" :key="cmt.pk">
        <Comment :comment="cmt" />
      </li>
    </ul>
  </div>
</template>
