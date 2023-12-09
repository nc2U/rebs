<script lang="ts" setup="">
import { ref } from 'vue'

const commentLength = ref(0)
</script>

<template>
  <div v-if="commentLength">
    <h5 class="my-4 ml-4">{{ commentLength }} Comments</h5>
    <ul v-for="i in commentLength" :key="i" class="comments mx-5 mb-4">
      <li>
        <div class="comment-item border-bottom-1">
          <strong>홍길동</strong>
          <small class="ml-2">2023-12-09 09:00:00</small>
          <small class="ml-2">추천 0 비추 0 신고</small>
          <p>댓글에 대한 테스트 컴포넌트입니다.</p>
        </div>
      </li>
    </ul>
  </div>
</template>
