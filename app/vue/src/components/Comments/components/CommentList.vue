<script lang="ts" setup="">
import { ref } from 'vue'
import Comment from './Comment.vue'

defineProps({
  commentList: { type: Object, default: () => [] },
})

const commentLength = ref(3)
</script>

<template>
  <div v-if="commentList?.length">
    <h5 class="my-4 ml-4">{{ commentList?.length }} Comments</h5>
    <ul class="comments mx-5 mb-4">
      <li v-for="i in commentList" :key="i">
        <Comment />
      </li>
    </ul>
  </div>
</template>
