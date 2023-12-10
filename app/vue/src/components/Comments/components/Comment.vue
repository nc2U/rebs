<script lang="ts" setup="">
import { computed, inject, type PropType } from 'vue'
import type { User } from '@/store/types/accounts'
import type { Comment as Cm } from '@/store/types/document'

const props = defineProps({ comment: Object as PropType<Cm>, default: null })

const userInfo = inject<User>('userInfo')
</script>

<template>
  <div class="comment-item border-bottom-1">
    <strong>{{ comment?.user.username }}</strong>
    <small class="ml-2">2023-12-09 09:00:00</small>
    <small class="ml-2">추천 0 비추 0 신고</small>
    <small class="ml-2">답변</small>
    <template v-if="userInfo?.pk === props.comment?.user.pk">
      <!--    해당 본인 작성글이고 댓글에 대댓글이 없을 경우 수정/삭제 활성-->
      <small class="ml-1">수정</small>
      <small class="ml-1">삭제</small>
    </template>

    <p>{{ comment?.content }}</p>
  </div>
</template>
