<script lang="ts" setup="">
import { nextTick, onMounted, onUpdated, type PropType, reactive } from 'vue'
import type { Comment as Cm } from '@/store/types/document'

const props = defineProps({
  post: { type: Number, required: true },
  comment: { type: Object as PropType<Cm>, default: null },
  parent: { type: Number, default: null },
})
const emit = defineEmits(['on-submit'])

// const show1 = ref(false)
const form = reactive<Cm>({
  pk: undefined,
  post: props.post,
  content: '',
  parent: props.parent,
  secret: false,
  password: '',
})

// const passwordRules = ref([
//   (value: string) => {
//     if (value?.length >= 2) return true
//     return 'Password must be at least 2 characters.'
//   },
// ])

const falseRemove = () =>
  nextTick(() => {
    if (form.secret) form.password = ''
  })

const onSubmit = () => {
  emit('on-submit', form)
  formReset()
}

const formReset = () => {
  form.pk = undefined
  form.content = ''
  form.parent = null
  form.secret = false
  form.password = ''
}

const formSet = () => {
  if (props.comment) {
    form.pk = props.comment.pk
    form.content = props.comment.content
    form.parent = props.comment.parent
    form.secret = props.comment.secret
    form.password = props.comment.password
  }
}

onMounted(() => formSet())
onUpdated(() => formSet())
</script>

<template>
  <v-form class="p-3 bg-light" @submit.prevent="onSubmit">
    <v-container fluid class="m-0 p-0">
      <v-textarea
        label="comment"
        v-model="form.content"
        auto-grow
        variant="outlined"
        rows="3"
        row-height="25"
        color="grey-lighten-1"
        base-color="grey-lighten-1"
        bg-color="white"
        shaped
        required
      />
      <v-row>
        <!--        <v-col class="d-flex" md="3">-->
        <!--          <v-text-field-->
        <!--            label="password"-->
        <!--            v-model="form.password"-->
        <!--            :rules="passwordRules"-->
        <!--            :type="show1 ? 'text' : 'password'"-->
        <!--            auto-grow-->
        <!--            variant="outlined"-->
        <!--            color="grey-lighten-1"-->
        <!--            base-color="grey-lighten-1"-->
        <!--            bg-color="white"-->
        <!--            shaped-->
        <!--            hide-details-->
        <!--            :disabled="!form.secret"-->
        <!--            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"-->
        <!--            @click:append="show1 = !show1"-->
        <!--          />-->
        <!--        </v-col>-->
        <v-checkbox
          label="Secret"
          v-model="form.secret"
          density="compact"
          hide-details
          class="m-3 pt-1"
          @click="falseRemove"
        />

        <v-col class="text-right pt-3">
          <v-btn
            type="submit"
            :color="!comment ? 'primary' : 'success'"
            tonal
            size="large"
            :disabled="!form.content"
          >
            댓글등록
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>
