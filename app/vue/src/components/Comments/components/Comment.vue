<script lang="ts" setup="">
import { inject, type PropType } from 'vue'
import { elapsedTime } from '@/utils/baseMixins'
import type { User } from '@/store/types/accounts'
import type { Comment as Cm } from '@/store/types/document'

const props = defineProps({ comment: Object as PropType<Cm>, default: null })

const userInfo = inject<User>('userInfo')

const toBlame = () => {
  if (confirm('이 댓글을 신고하시겠습니까?\n\n한번 신고하신 후에는 취소가 불가능합니다.'))
    alert('ok!')
}

const toLike = () => alert('reply')
const toDisLike = () => alert('reply')
const toReply = () => alert('reply')
const toModify = () => alert('modify')
const toDelete = () => alert('delete')
</script>

<template>
  <div class="comment-item text-black-50">
    <strong>{{ comment?.user?.username }}</strong>
    <small class="ml-2">{{ elapsedTime(comment?.updated ?? '') }}</small>
    <small class="ml-2 text-btn" @click="toLike">
      <v-icon icon="mdi mdi-thumb-up" size="xs" />
      추천 {{ comment?.like ?? 0 }}
    </small>
    <small class="ml-1 text-btn" @click="toDisLike">
      <v-icon icon="mdi mdi-thumb-down" size="xs" />
      비추 {{ comment?.dislike ?? 0 }}
    </small>
    <small class="ml-2 text-btn" @click="toBlame">
      <v-icon icon="mdi mdi-bell" size="xs" />
      <v-tooltip activator="parent" location="end">신고하기</v-tooltip>
    </small>
    <small class="ml-2 text-btn" @click="toReply">답변</small>
    <template v-if="userInfo?.pk === props.comment?.user?.pk">
      <!--    해당 본인 작성글이고 댓글에 대댓글이 없을 경우 수정/삭제 활성-->
      <small class="ml-1 text-btn" @click="toModify">수정</small>
      <small class="ml-1 text-btn" @click="toDelete">삭제</small>
    </template>

    <p>{{ comment?.content }}</p>
  </div>
</template>
