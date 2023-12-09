<script lang="ts" setup="">
import { ref } from 'vue'
import Comment from './Comment.vue'

const commentLength = ref(3)
</script>

<template>
  <div v-if="commentLength">
    <h5 class="my-4 ml-4">{{ commentLength }} Comments</h5>
    <ul class="comments mx-5 mb-4">
      <li v-for="i in commentLength" :key="i">
        <Comment />
      </li>
    </ul>
  </div>
</template>
