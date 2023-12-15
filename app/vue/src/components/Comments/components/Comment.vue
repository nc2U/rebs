<script lang="ts" setup>
import { ref, inject, type ComputedRef, type PropType, watch, computed } from 'vue'
import { elapsedTime } from '@/utils/baseMixins'
import type { User } from '@/store/types/accounts'
import type { Comment as Cm } from '@/store/types/document'
import CommentForm from './CommentForm.vue'

const props = defineProps({
  formShow: { type: Boolean, default: true }, // 현재 댓글과 편집 폼 댓글이 동일한지 여부
  comment: { type: Object as PropType<Cm>, default: null },
  likeComments: { type: Array as PropType<number[]>, default: () => [] },
  lastDepth: { type: Boolean, default: false },
})

watch(props, val => {
  if (!val.formShow) {
    // 현재 편집폼이 아니면 초기화
    isReplying.value = false
    isEditing.value = false
  }
})

const emit = defineEmits(['vision-toggle', 'to-like', 'on-submit'])

const userInfo = inject<ComputedRef<User>>('userInfo')

const isLike = computed(() => props.likeComments.includes(props.comment.pk ?? 0))

const isReplying = ref<boolean>(false)
const isEditing = ref<boolean>(false)

const toBlame = () => {
  if (confirm('이 댓글을 신고하시겠습니까?\n\n한번 신고하신 후에는 취소가 불가능합니다.'))
    alert('ok!')
}

const toLike = () => emit('to-like', props.comment.pk)

const toReply = () => {
  isEditing.value = false
  isReplying.value = !isReplying.value
  emit('vision-toggle', { num: props.comment?.pk as number, sts: !isReplying.value })
}

const toModify = () => {
  isReplying.value = false
  isEditing.value = !isEditing.value
  emit('vision-toggle', { num: props.comment?.pk as number, sts: !isEditing.value })
}

const toDelete = () => alert('delete')

const onSubmit = (payload: Cm) => emit('on-submit', payload)
</script>

<template>
  <li class="text-50">
    <strong>{{ comment?.user?.username }}</strong>
    <small class="ml-2">
      <v-icon icon="mdi-clock-time-four-outline" size="sm" />
      {{ elapsedTime(comment?.created ?? '') }}
    </small>
    <small class="ml-2">
      <v-icon
        :icon="isLike ? 'mdi-heart' : 'mdi-heart-outline'"
        @click="toLike"
        size="sm"
        class="icon-btn"
      />
      {{ !isLike ? '좋아요' : '취소' }}
      {{ comment?.like ?? 0 }}
    </small>
    <small class="ml-2 text-btn" @click="toBlame">
      <v-icon icon="mdi mdi-bell" size="xs" />
      <v-tooltip activator="parent" location="end">신고하기</v-tooltip>
    </small>
    <small v-if="!lastDepth" class="ml-2 text-btn" @click="toReply">
      {{ !isReplying ? '답변' : '취소' }}
    </small>
    <template v-if="!comment.replies?.length && userInfo?.pk === props.comment?.user?.pk">
      <!--    해당 본인 작성글이고 댓글에 대댓글이 없을 경우 수정/삭제 활성-->
      <small class="ml-1 text-btn" @click="toModify">
        {{ !isEditing ? '수정' : '취소' }}
      </small>
      <small class="ml-1 text-btn" @click="toDelete">삭제</small>
    </template>

    <p v-if="!(formShow && isEditing)">
      <CBadge v-if="comment.secret" color="warning" class="mr-1">비밀글입니다</CBadge>
      <span v-show="!comment.secret || userInfo?.is_superuser || userInfo?.pk === comment.user?.pk">
        {{ comment?.content }}
      </span>
    </p>
    <p v-if="formShow && isEditing">
      <!-- 수정시 -->
      <CommentForm :post="comment?.post as number" :comment="comment" @on-submit="onSubmit" />
    </p>
    <p v-if="formShow && isReplying">
      <!-- 답변시 -->
      <CommentForm
        :post="comment?.post as number"
        :parent="comment?.pk as number"
        @on-submit="onSubmit"
      />
    </p>
  </li>
</template>

<style lang="scss" scoped>
li {
  list-style-type: none;
}
</style>
