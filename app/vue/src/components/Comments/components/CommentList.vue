<script lang="ts" setup="">
import type { PropType } from 'vue'
import type { Comment as Cm } from '@/store/types/document'
import Comment from './Comment.vue'

defineProps({
  actForm: { type: Number, default: undefined },
  comments: { type: Array as PropType<Cm[]>, default: () => [] },
})
const emit = defineEmits(['vision-toggle', 'on-submit', 'form-reset'])

const visionToggle = (payload: { num: number; sts: boolean }) => emit('vision-toggle', payload)

const onSubmit = (payload: Cm) => {
  emit('on-submit', payload)
  emit('form-reset')
}
</script>

<template>
  <div v-if="comments.length">
    <h5 class="my-4 ml-4">{{ comments.length }} Comments</h5>
    <ul class="comments mx-5 mb-4">
      <li v-for="cmt in comments" :key="cmt.pk">
        <Comment
          :form-show="actForm === cmt.pk"
          :comment="cmt"
          @vision-toggle="visionToggle"
          @on-submit="onSubmit"
        />
      </li>
    </ul>
  </div>
</template>
