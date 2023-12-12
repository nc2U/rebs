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
    <ul v-for="cmt1 in comments" :key="cmt1.pk" class="comments ml-5 mb-4">
      <Comment
        :form-show="actForm === cmt1.pk"
        :comment="cmt1"
        @vision-toggle="visionToggle"
        @on-submit="onSubmit"
      />

      <ul v-for="cmt2 in cmt1.replies" :key="cmt2.pk" class="comments ml-5 mb-4">
        <Comment
          :form-show="actForm === cmt2.pk"
          :comment="cmt2"
          @vision-toggle="visionToggle"
          @on-submit="onSubmit"
        />

        <ul v-for="cmt3 in cmt2.replies" :key="cmt3.pk" class="comments ml-5 mb-4">
          <Comment
            :form-show="actForm === cmt3.pk"
            :comment="cmt3"
            @vision-toggle="visionToggle"
            @on-submit="onSubmit"
          />

          <ul v-for="cmt4 in cmt3.replies" :key="cmt4.pk" class="comments ml-5 mb-4">
            <Comment
              :form-show="actForm === cmt4.pk"
              :comment="cmt4"
              @vision-toggle="visionToggle"
              @on-submit="onSubmit"
            />
            <ul v-for="cmt5 in cmt4.replies" :key="cmt5.pk" class="comments ml-5 mb-4">
              <Comment
                :form-show="actForm === cmt5.pk"
                :comment="cmt5"
                :last-depth="true"
                @vision-toggle="visionToggle"
                @on-submit="onSubmit"
              />
            </ul>
          </ul>
        </ul>
      </ul>
    </ul>
  </div>
</template>
