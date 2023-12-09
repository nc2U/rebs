<script lang="ts" setup="">
import { ref } from 'vue'

const comment = ref({
  user: {
    name: '홍길동',
  },
  contents: '댓글에 대한 테스트 컴포넌트입니다.',
})
</script>

<template>
  <div class="comment-item border-bottom-1">
    <strong>{{ comment.user.name }}</strong>
    <small class="ml-2">2023-12-09 09:00:00</small>
    <small class="ml-2">추천 0 비추 0 신고</small>
    <p>{{ comment.contents }}</p>
    <!--    <ul>-->
    <!--      <li>-->
    <!--        <button type="button">수정</button>-->
    <!--        <button type="button">삭제</button>-->
    <!--      </li>-->
    <!--    </ul>-->
  </div>
</template>
