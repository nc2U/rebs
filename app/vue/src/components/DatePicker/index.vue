<script lang="ts" setup>
import { ref, reactive, computed } from 'vue'
import { useStore } from 'vuex'
import Datepicker from '@vuepic/vue-datepicker'

const store = useStore()
const isDark = computed(() => store.state.theme === 'dark')

const textInputOptions = ref({
  enterSubmit: true,
  tabSubmit: true,
  openMenu: true,
  format: 'yyyy-MM-dd',
})

const dateOptions = reactive({
  mask: '####-##-##',
  eager: true,
})
</script>

<template>
  <Datepicker
    v-maska:[dateOptions]
    text-input
    auto-apply
    format="yyyy-MM-dd"
    position="left"
    :text-input-options="textInputOptions"
    input-class-name="form-control"
    :enable-time-picker="false"
    :teleport="true"
    :dark="isDark"
    locale="ko"
    allow-prevent-default
  />
</template>
