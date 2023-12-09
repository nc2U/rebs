<script lang="ts" setup="">
import { ref, nextTick } from 'vue'

const show1 = ref(false)
const form = ref({
  content: '',
  password: '',
  secret: false,
})

const passwordRules = ref([
  (value: string) => {
    if (value?.length >= 2) return true
    return 'Password must be at least 2 characters.'
  },
])

const falseRemove = () =>
  nextTick(() => {
    if (form.value.secret) form.value.password = ''
  })

const onSubmit = () => alert('submitted!')
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
        <v-col class="d-flex" md="3">
          <v-text-field
            label="password"
            v-model="form.password"
            :rules="passwordRules"
            :type="show1 ? 'text' : 'password'"
            auto-grow
            variant="outlined"
            color="grey-lighten-1"
            base-color="grey-lighten-1"
            bg-color="white"
            shaped
            hide-details
            :disabled="!form.secret"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="show1 = !show1"
          />
        </v-col>
        <v-checkbox
          label="Secret"
          v-model="form.secret"
          density="compact"
          hide-details
          class="m-3 pt-1"
          @click="falseRemove"
        />

        <v-col class="text-right pt-3">
          <v-btn type="submit" color="primary" tonal size="large" :disabled="!form.content">
            댓글등록
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>
