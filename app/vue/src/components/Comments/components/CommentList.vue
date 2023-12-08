<script lang="ts" setup="">
import { ref } from 'vue'

const msg = ref('Hello world')
</script>

<template>
  <div v-if="1 == 1">
    <h5 class="my-4 ml-4">1 Comments</h5>
    <ul class="comments mx-5 mb-4">
      <li>
        <div class="comment-item">
          <strong>홍길동</strong> <small>2023-12-09</small>
          <p>댓글에 대한 테스트 컴포넌트입니다.</p>
        </div>
      </li>

      <li>
        <div class="comment-item">
          <strong>홍길동</strong> <small>2023-12-09</small>
          <p>댓글에 대한 테스트 컴포넌트입니다.</p>
        </div>
      </li>

      <li>
        <div class="comment-item">
          <strong>홍길동</strong> <small>2023-12-09</small>
          <p>댓글에 대한 테스트 컴포넌트입니다.</p>
        </div>
      </li>
    </ul>
  </div>
</template>
