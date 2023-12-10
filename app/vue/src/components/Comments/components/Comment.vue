<script lang="ts" setup="">
import { type PropType } from 'vue'
import type { Comment as Cm } from '@/store/types/document'

defineProps({ comment: Object as PropType<Cm>, default: null })
</script>

<template>
  <div class="comment-item border-bottom-1">
    <strong>{{ comment?.user }}</strong>
    <small class="ml-2">2023-12-09 09:00:00</small>
    <small class="ml-2">추천 0 비추 0 신고</small>
    <p>{{ comment?.content }}</p>
    <!--    <ul>-->
    <!--      <li>-->
    <!--        <button type="button">수정</button>-->
    <!--        <button type="button">삭제</button>-->
    <!--      </li>-->
    <!--    </ul>-->
  </div>
</template>
