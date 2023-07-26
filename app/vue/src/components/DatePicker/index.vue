<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import Datepicker from '@vuepic/vue-datepicker'

const store = useStore()
const isDark = computed(() => store.state.theme === 'dark')

const options = ref({ format: 'yyyy-MM-dd' })
</script>

<template>
  <Datepicker
    locale="ko"
    auto-apply
    text-input
    :dark="isDark"
    position="left"
    :teleport="true"
    format="yyyy-MM-dd"
    model-type="format"
    placeholder="날짜선택"
    allow-prevent-default
    :enable-time-picker="false"
    :text-input-options="options"
    input-class-name="form-control"
  />
</template>
